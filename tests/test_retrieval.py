import os

import pytest
from langchain_core.documents import Document
from langchain_chroma import Chroma

from src.policy_rag import retrieve_policy


def test_metadata_filter_excludes_wrong_pathways(
    tmp_path, fake_embeddings
):
    documents = [
        Document(
            page_content="Adults require BMI 35 and six months of lifestyle treatment.",
            metadata={
                "section_type": "active",
                "section": "COVERAGE CRITERIA",
                "indication": "Chronic Weight Management (Adult)",
            },
        ),
        Document(
            page_content="Continuation therapy requires maintained weight loss.",
            metadata={
                "section_type": "active",
                "section": "CONTINUATION OF THERAPY",
                "indication": "Chronic Weight Management (Adult)",
            },
        ),
        Document(
            page_content="Pediatric patients must be between 12 and 17.",
            metadata={
                "section_type": "active",
                "section": "COVERAGE CRITERIA",
                "indication": "Chronic Weight Management (Pediatric)",
            },
        ),
        Document(
            page_content="An outdated historical policy requirement.",
            metadata={
                "section_type": "history",
                "section": "HISTORY",
                "indication": "Chronic Weight Management (Adult)",
            },
        ),
    ]

    store = Chroma.from_documents(
        documents=documents,
        embedding=fake_embeddings,
        collection_name="retrieval_test",
        persist_directory=str(tmp_path / "chroma"),
    )

    results = retrieve_policy(
        "Adult initial authorization BMI requirements",
        store,
        section="COVERAGE CRITERIA",
        indication="Chronic Weight Management (Adult)",
    )

    assert len(results) == 1

    document, distance = results[0]

    assert "Adults require BMI 35" in document.page_content
    assert document.metadata["section_type"] == "active"
    assert document.metadata["section"] == "COVERAGE CRITERIA"
    assert isinstance(distance, (float, int))


def test_history_excluded_by_default(tmp_path, fake_embeddings):
    documents = [
        Document(
            page_content="Active BMI coverage requirement.",
            metadata={"section_type": "active"},
        ),
        Document(
            page_content="Old BMI coverage requirement.",
            metadata={"section_type": "history"},
        ),
    ]

    store = Chroma.from_documents(
        documents=documents,
        embedding=fake_embeddings,
        collection_name="history_test",
        persist_directory=str(tmp_path / "chroma"),
    )

    results = retrieve_policy("BMI requirements", store, k=5)

    assert len(results) == 1
    assert results[0][0].metadata["section_type"] == "active"


@pytest.mark.integration
def test_real_aetna_retrieval():
    """Optional test using the existing Aetna index and real embedding model."""

    if os.getenv("RUN_RAG_INTEGRATION") != "1":
        pytest.skip("Set RUN_RAG_INTEGRATION=1 to run the real retrieval test")

    from pathlib import Path
    from langchain_huggingface import HuggingFaceEmbeddings

    database_path = Path("data/chroma_db")

    assert database_path.exists(), "Aetna ChromaDB index not found"

    embeddings = HuggingFaceEmbeddings(
        model_name="ethanteh/bge-finetuned-insurance-matryoshka",
        model_kwargs={"device": "cpu"},
    )

    store = Chroma(
        collection_name="aetna_policy",
        embedding_function=embeddings,
        persist_directory=str(database_path),
    )

    assert store._collection.count() > 0

    results = retrieve_policy(
        "Wegovy adult chronic weight management initial authorization BMI and lifestyle program requirements",
        store,
        section="COVERAGE CRITERIA",
        indication="Chronic Weight Management (Adult)",
    )

    assert results

    document, distance = results[0]
    text = document.page_content.lower()

    assert "18 years" in text
    assert "6 months" in text
    assert "35" in text
    assert document.metadata["section"] == "COVERAGE CRITERIA"
    assert distance >= 0
