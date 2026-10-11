import re

from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

MODEL_NAME = "ethanteh/bge-finetuned-insurance-matryoshka"

BASE_DIR = Path(__file__).resolve().parent.parent

def chunk_policy(policy_text: str) -> list[Document]:
    """Chunk policy text by headings, then split oversized sections."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " "],
        length_function=len,
    )

    sections = []
    current_lines = []
    section = "Policy Introduction"
    medication = ""
    indication = ""
    pathway = ""
    section_type = "active"

    lines = policy_text.splitlines()

    for i, line in enumerate(lines):
        heading = line.strip()

        major_heading = re.match(
            r"^(COVERAGE CRITERIA|CONTINUATION OF THERAPY|"
            r"QUANTITY LIMITS APPLY|DURATION OF APPROVAL.*|"
            r"FDA-APPROVED INDICATIONS|OVERVIEW|"
            r"POLICY STATEMENT|HISTORY(?: \(CONTINUED\))?|"
            r"Section \d+:.*|General Coverage Criteria|"
            r"Coverage Criteria for North Dakota.*)$",
            heading,
            re.IGNORECASE,
        )

        roman_heading = re.fullmatch(
            r"[IVXLCDM]+\.",
            heading,
        )

        subsection_heading = re.match(
            r"^(Chronic Weight Management \(.*|"
            r"Risk Reduction of Major Adverse Cardiovascular Events.*|"
            r"\d+\.\s+(?:Weight Loss|Obstructive Sleep Apnea|"
            r"Metabolic Dysfunction|Major Adverse Cardiovascular).*)$",
            heading,
            re.IGNORECASE,
        )

        pathway_heading = re.match(
            r"^[A-Z][).]\s+(?:Initial Therapy|"
            r"Patient is Currently Receiving|"
            r"Initial Authorization|Reauthorization|"
            r"Continuation Therapy).*",
            heading,
        )

        is_heading = (
            major_heading
            or roman_heading
            or subsection_heading
            or pathway_heading
        )

        if is_heading:

            if current_lines and any(text.strip() for text in current_lines):
                sections.append(Document(
                    page_content="\n".join(current_lines),
                    metadata={
                        "section": section,
                        "medication": medication,
                        "indication": indication,
                        "pathway": pathway,
                        "section_type": section_type,
                    },
                ))

            current_lines = []

            if roman_heading:
                section = heading
                indication = ""
                pathway = ""

                following_text = " ".join(lines[i + 1:i + 6])

                drug_match = re.search(
                    r"\b(Liraglutide|Foundayo|"
                    r"Wegovy(?: HD)?(?: injection| tablet)?|"
                    r"Zepbound)\b",
                    following_text[:300],
                    re.IGNORECASE,
                )

                medication = drug_match.group(1) if drug_match else ""

            elif major_heading:

                if re.match(r"^HISTORY", heading, re.IGNORECASE):
                    section_type = "history"
                    section = heading
                    medication = ""
                    indication = ""
                    pathway = ""

                elif heading.lower() == "fda-approved indications":
                    pass

                else:
                    section = heading
                    medication = ""
                    indication = ""
                    pathway = ""

            elif subsection_heading:
                indication = heading
                pathway = ""

            elif pathway_heading:
                pathway = heading

        current_lines.append(line)

    if current_lines:
        sections.append(Document(
            page_content="\n".join(current_lines),
            metadata={
                "section": section,
                "medication": medication,
                "indication": indication,
                "pathway": pathway,
                "section_type": section_type,
            },
        ))

    chunks = []

    for section_document in sections:
        if len(section_document.page_content) > 1500:
            chunks.extend(text_splitter.split_documents([section_document]))
        else:
            chunks.append(section_document)

    return chunks


def ingest_policy(chunks: list[Document], payer: str):
    """Embed policy chunks and store them in ChromaDB."""

    embeddings = HuggingFaceEmbeddings(
        model_name="ethanteh/bge-finetuned-insurance-matryoshka",
        model_kwargs={"device": "cpu"},
    )

    for chunk in chunks:
        chunk.metadata["payer"] = payer

    vector_store = Chroma(
        collection_name=f"{payer}_policy",
        embedding_function=embeddings,
        persist_directory="data/chroma_db",
    )

    vector_store.reset_collection()
    vector_store.add_documents(chunks)

    return vector_store


def retrieve_policy(
    query: str,
    vector_store: Chroma,
    k: int = 5,
    section: str | None = None,
    indication: str | None = None,
):
    """Retrieve relevant policy chunks with optional metadata filters."""

    filters = [{"section_type": "active"}]

    if section:
        filters.append({"section": section})

    if indication:
        filters.append({"indication": indication})

    search_filter = filters[0] if len(filters) == 1 else {"$and": filters}

    results = vector_store.similarity_search_with_score(
        query=query,
        k=k,
        filter=search_filter,
    )

    return results


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent

    policy_files = {
        "aetna": BASE_DIR / "data" / "policies" / "policies_txt" / "aetna_glp1_weight_management.txt",
        "cigna": BASE_DIR / "data" / "policies" / "policies_txt" / "cigna_glp1_prior_auth.txt",
        "unitedhealthcare": BASE_DIR / "data" / "policies" / "policies_txt" / "uhc_weight_loss_prior_auth.txt",
    }

    for payer, file_path in policy_files.items():
        policy_text = file_path.read_text(encoding="utf-8")

        chunks = chunk_policy(policy_text)

        if payer in ["cigna", "unitedhealthcare"]:
            vector_store = ingest_policy(chunks, payer)

            print(f"\n{payer.upper()}")
            print(f"Expected chunks: {len(chunks)}")
            print(f"Stored records: {vector_store._collection.count()}")
