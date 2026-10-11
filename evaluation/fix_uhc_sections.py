import json
import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from evaluation.evaluate_retrieval import evaluate_query
from evaluation.experiment_contextual_cigna import ranking_metrics, summarize


BASE_DIR = Path(__file__).resolve().parent.parent
POLICY_FILE = BASE_DIR / "data/policies/policies_txt/uhc_weight_loss_prior_auth.txt"
DATABASE_DIR = BASE_DIR / "data/chroma_db"
RESULTS_DIR = BASE_DIR / "evaluation/results"
QUERIES_FILE = BASE_DIR / "evaluation/retrieval_queries.json"
BASELINE_FILE = RESULTS_DIR / "retrieval_evaluation.json"

COLLECTION_NAME = "unitedhealthcare_policy_context_v3"
MODEL_NAME = "ethanteh/bge-finetuned-insurance-matryoshka"


def chunk_uhc_policy(policy_text: str) -> list[Document]:
    """Separate UHC coverage scopes and authorization pathways."""

    # Find the actual coverage criteria, not headings in Section Overview.
    general_match = re.search(
        r"(?im)^[ \t]*Coverage Criteria[a-z]?:[ \t\u00a0]*$",
        policy_text,
    )

    nd_match = re.search(
        r"(?im)^[ \t]*Coverage Criteria for North Dakota "
        r"Fully Insured EHB.*$",
        policy_text,
    )

    if not general_match or not nd_match:
        raise ValueError(
            "Could not identify both actual UHC coverage sections. "
            "No collection will be changed."
        )

    if general_match.start() >= nd_match.start():
        raise ValueError(
            "Unexpected UHC section order. No collection will be changed."
        )

    # The active North Dakota criteria end before Additional Clinical Rules.
    remainder = policy_text[nd_match.start():]

    end_match = re.search(
        r"(?im)^[ \t]*4\.[ \t]*$"
        r"\s*Additional Clinical Rules:",
        remainder,
    )

    if not end_match:
        raise ValueError(
            "Could not identify the end of North Dakota coverage criteria. "
            "No collection will be changed."
        )

    nd_end = nd_match.start() + end_match.start()

    coverage_sections = {
        "general": policy_text[
            general_match.start():nd_match.start()
        ],
        "north_dakota": policy_text[
            nd_match.start():nd_end
        ],
    }

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " "],
        length_function=len,
    )

    documents = []

    for scope, section_text in coverage_sections.items():

        initial_match = re.search(
            r"(?im)^[ \t]*A\.[ \t]+Initial Authorization\b",
            section_text,
        )

        reauth_match = re.search(
            r"(?im)^[ \t]*B\.[ \t]+Reauthorization\b",
            section_text,
        )

        if not initial_match or not reauth_match:
            raise ValueError(
                f"Missing authorization pathway in {scope}. "
                "No collection will be changed."
            )

        if initial_match.start() >= reauth_match.start():
            raise ValueError(
                f"Unexpected pathway order in {scope}."
            )

        pathways = {
            "Initial Authorization": section_text[
                initial_match.start():reauth_match.start()
            ],
            "Reauthorization": section_text[
                reauth_match.start():
            ],
        }

        section_name = (
            "North Dakota Fully Insured EHB"
            if scope == "north_dakota"
            else "General Coverage Criteria"
        )

        for pathway, pathway_text in pathways.items():

            original_chunks = splitter.split_text(pathway_text)

            for chunk_number, original_text in enumerate(original_chunks):

                metadata = {
                    "payer": "unitedhealthcare",
                    "scope": scope,
                    "section": section_name,
                    "medication": "",
                    "indication": "",
                    "pathway": pathway,
                    "section_type": "active",
                    "chunk_number": chunk_number,
                    "original_text": original_text,
                }

                contextual_text = (
                    "Insurance provider: UnitedHealthcare\n"
                    f"Coverage scope: {section_name}\n"
                    f"Authorization pathway: {pathway}\n\n"
                    f"{original_text}"
                )

                documents.append(
                    Document(
                        page_content=contextual_text,
                        metadata=metadata,
                    )
                )

    return documents


def main():
    policy_text = POLICY_FILE.read_text(encoding="utf-8")

    print("Parsing UHC coverage sections...")

    chunks = chunk_uhc_policy(policy_text)

    counts = {}

    for chunk in chunks:
        key = (
            chunk.metadata["scope"],
            chunk.metadata["pathway"],
        )
        counts[key] = counts.get(key, 0) + 1

    print("\nSECTION COUNTS")

    for (scope, pathway), count in counts.items():
        print(f"{scope} | {pathway}: {count} chunks")

    expected_groups = {
        ("general", "Initial Authorization"),
        ("general", "Reauthorization"),
        ("north_dakota", "Initial Authorization"),
        ("north_dakota", "Reauthorization"),
    }

    assert set(counts) == expected_groups

    # Check that historical material was not indexed.
    assert not any(
        "9/2021" in chunk.metadata["original_text"]
        and "9/2022" in chunk.metadata["original_text"]
        for chunk in chunks
    )

    print(f"\nTotal active chunks: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"},
    )

    store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(DATABASE_DIR),
    )

    # Only V3 is reset. V1 and V2 are preserved.
    store.reset_collection()
    store.add_documents(chunks)

    assert store._collection.count() == len(chunks)

    print(f"Stored {store._collection.count()} chunks in {COLLECTION_NAME}")

    cases = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))
    uhc_cases = [
        case for case in cases
        if case["payer"] == "unitedhealthcare"
    ]

    results = []

    print("\nUHC V3 RETRIEVAL TEST")

    for case in uhc_cases:
        # Search the entire active UHC V3 index, without providing
        # the expected pathway as a retrieval filter.
        matches = store.similarity_search_with_score(
            case["query"],
            k=5,
            filter={"section_type": "active"},
        )

        expected_pathway = (
            "Initial Authorization"
            if case["id"] == "UHC-01"
            else "Reauthorization"
        )

        relevant = 0
        ranked = []

        for rank, (document, distance) in enumerate(matches, start=1):
            correct = (
                document.metadata["scope"] == "north_dakota"
                and document.metadata["pathway"] == expected_pathway
            )

            relevant += int(correct)

            ranked.append({
                "rank": rank,
                "distance": round(float(distance), 4),
                "relevant": correct,
                "scope": document.metadata["scope"],
                "pathway": document.metadata["pathway"],
                "text_preview": document.metadata["original_text"][:200],
            })

            print(
                f"{case['id']} Rank {rank}: "
                f"{document.metadata['scope']} | "
                f"{document.metadata['pathway']} | "
                f"distance={distance:.4f} | "
                f"correct={correct}"
            )

        relevant_total = sum(
            count for (scope, pathway), count in counts.items()
            if scope == "north_dakota"
            and pathway == expected_pathway
        )

        relevant_ranks = [
            item["rank"] for item in ranked if item["relevant"]
        ]

        results.append({
            "id": case["id"],
            "query": case["query"],
            "relevant_chunks_in_index": relevant_total,
            "relevant_retrieved": relevant,
            "hit_at_5": relevant > 0,
            "recall_at_5": round(relevant / relevant_total, 4),
            "precision_at_5": round(relevant / 5, 4),
            "mrr_at_5": round(
                1 / relevant_ranks[0] if relevant_ranks else 0, 4
            ),
            "results": ranked,
        })

    report = {
        "experiment": "UHC V3 coverage-scope parsing",
        "collection": COLLECTION_NAME,
        "total_chunks": len(chunks),
        "section_counts": {
            f"{scope}/{pathway}": count
            for (scope, pathway), count in counts.items()
        },
        "note": (
            "This evaluates scope/pathway correctness using parser labels. "
            "It does not independently verify all clinical requirements."
        ),
        "queries": results,
    }

    output = RESULTS_DIR / "uhc_v3_evaluation.json"
    output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nSUMMARY")

    for result in results:
        print(
            f"{result['id']}: "
            f"Hit@5={result['hit_at_5']} | "
            f"Recall@5={result['recall_at_5']:.2%} | "
            f"MRR@5={result['mrr_at_5']:.2f}"
        )

    print(f"\nSaved evaluation: {output}")


if __name__ == "__main__":
    main()
