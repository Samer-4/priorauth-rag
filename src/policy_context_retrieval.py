"""Validated policy-context retrieval for the Stage 2 RAG adapter.

Uses existing experimental Chroma collections.
Does not modify the collections or the six-stage pipeline.
"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data/chroma_db"

EMBEDDING_MODEL = "ethanteh/bge-finetuned-insurance-matryoshka"

COLLECTIONS = {
    "aetna": "aetna_policy_context_v2",
    "cigna": "cigna_policy_context_v2",
    "unitedhealthcare": "unitedhealthcare_policy_context_v3",
}


class PolicyRetrievalError(ValueError):
    """Raised when safe, unambiguous retrieval is not possible."""


@dataclass(frozen=True)
class PolicyContext:
    payer: str
    collection: str
    query: str
    passages: tuple[str, ...]
    metadata: tuple[dict, ...]

    @property
    def policy_text(self) -> str:
        return "\n\n".join(self.passages)


@lru_cache(maxsize=1)
def _embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
    )


def _store(payer: str):
    return Chroma(
        collection_name=COLLECTIONS[payer],
        embedding_function=_embeddings(),
        persist_directory=str(DB_PATH),
    )


def _contains(value, expected):
    return str(expected).casefold() in str(value or "").casefold()


def _match(metadata, payer, medication, indication, pathway, scope):
    if metadata.get("section_type") != "active":
        return False

    if payer == "aetna":
        expected_section = (
            "COVERAGE CRITERIA"
            if pathway == "initial"
            else "CONTINUATION OF THERAPY"
        )

        return (
            metadata.get("section") == expected_section
            and _contains(metadata.get("indication"), indication)
        )

    if payer == "cigna":
        expected_pathway = (
            "Initial Therapy"
            if pathway == "initial"
            else "Currently Receiving"
        )

        return (
            str(metadata.get("medication", "")).casefold()
            == medication.casefold()
            and _contains(metadata.get("indication"), indication)
            and _contains(metadata.get("pathway"), expected_pathway)
        )

    expected_pathway = (
        "Initial Authorization"
        if pathway == "initial"
        else "Reauthorization"
    )

    return (
        metadata.get("scope") == scope
        and metadata.get("pathway") == expected_pathway
    )


def retrieve_policy_context(
    *,
    payer: str,
    medication: str,
    indication: str,
    pathway: str,
    scope: str | None = None,
    query: str | None = None,
) -> PolicyContext:
    """Return authoritative passages from one explicitly selected pathway.

    pathway: 'initial' or 'continuation'
    scope for UHC: 'general' or 'north_dakota'

    Caller must establish coverage details from reliable case/plan data.
    Never infer a coverage scope from vector similarity.
    """

    payer = payer.strip().casefold()
    medication = medication.strip()
    indication = indication.strip()
    pathway = pathway.strip().casefold()

    if payer not in COLLECTIONS:
        raise PolicyRetrievalError(f"Unsupported payer: {payer}")

    if not medication or not indication:
        raise PolicyRetrievalError(
            "Medication and indication are required."
        )

    if pathway not in {"initial", "continuation"}:
        raise PolicyRetrievalError(
            "Pathway must be 'initial' or 'continuation'."
        )

    if payer == "unitedhealthcare":
        if scope not in {"general", "north_dakota"}:
            raise PolicyRetrievalError(
                "UHC requires an explicitly verified scope: "
                "'general' or 'north_dakota'."
            )
    elif scope is not None:
        raise PolicyRetrievalError(
            "Scope is only supported for UnitedHealthcare."
        )

    # UHC V3 currently groups some medications within the same pathway.
    # Do not assume every medication mentioned in that pathway is applicable.
    # Until indication/medication-specific conditions are fully validated,
    # restrict this adapter to manually reviewed UHC Wegovy requests.
    if payer == "unitedhealthcare":
        if medication.casefold() not in {
            "wegovy", "wegovy injection", "wegovy tablet"
        }:
            raise PolicyRetrievalError(
                "UHC medication has not been validated for this adapter."
            )

        if not _contains(indication, "weight loss"):
            raise PolicyRetrievalError(
                "UHC adapter currently supports reviewed weight-loss "
                "requests only."
            )

    if payer == "aetna" and not _contains(indication, "adult"):
        raise PolicyRetrievalError(
            "Aetna adapter currently supports reviewed adult pathways only."
        )

    if payer == "cigna" and not _contains(indication, "adult"):
        raise PolicyRetrievalError(
            "Cigna adapter currently supports reviewed adult pathways only."
        )

    store = _store(payer)

    if store._collection.count() == 0:
        raise PolicyRetrievalError(
            f"Missing or empty collection: {COLLECTIONS[payer]}"
        )

    records = store.get(
        where={"section_type": "active"},
        include=["metadatas", "documents"],
    )

    matches = []

    for index, metadata in enumerate(records["metadatas"]):
        if not _match(
            metadata, payer, medication, indication, pathway, scope
        ):
            continue

        original = metadata.get("original_text")

        if not isinstance(original, str) or not original.strip():
            raise PolicyRetrievalError(
                "Matched chunk is missing original policy text."
            )

        # The original text must be the suffix of the embedded document.
        # This verifies that we are retrieving text from the indexed source
        # rather than accidentally passing contextual headers as policy.
        embedded = records["documents"][index]

        if not isinstance(embedded, str) or not embedded.endswith(original):
            raise PolicyRetrievalError(
                "Original text does not match indexed document."
            )

        matches.append(
            (
                metadata,
                original,
                records["ids"][index],
            )
        )

    if not matches:
        raise PolicyRetrievalError(
            "No chunks matched the requested policy pathway. "
            "Review metadata and coverage details; no fallback was used."
        )

    # Preserve document order for UHC V3 multi-chunk pathways.
    if payer == "unitedhealthcare":
        matches.sort(
            key=lambda item: item[0].get("chunk_number", 0)
        )
    else:
        # Chroma IDs are not dependable source-order keys.
        # Existing V2 indexes do not store explicit sequence numbers.
        # For Aetna/Cigna, reject a pathway split across multiple chunks
        # until source-order metadata or parent-section assembly is added.
        if len(matches) > 1:
            raise PolicyRetrievalError(
                f"{payer} pathway matches {len(matches)} chunks, "
                "but source order is not verified. "
                "Refusing to concatenate potentially unordered criteria."
            )

    passages = tuple(item[1] for item in matches)

    if query is None:
        query = f"{payer} {medication} {indication} {pathway}"

    return PolicyContext(
        payer=payer,
        collection=COLLECTIONS[payer],
        query=query,
        passages=passages,
        metadata=tuple(item[0] for item in matches),
    )
