import src.policy_rag as policy_rag
from langchain_core.documents import Document


def test_ingestion_stores_all_chunks(tmp_path, monkeypatch, fake_embeddings):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        policy_rag,
        "HuggingFaceEmbeddings",
        lambda **kwargs: fake_embeddings,
    )

    chunks = [
        Document(
            page_content=f"Test coverage requirement {i}",
            metadata={"section_type": "active"},
        )
        for i in range(3)
    ]

    store = policy_rag.ingest_policy(chunks, "test_payer")

    assert store._collection.count() == 3


def test_repeated_ingestion_does_not_duplicate(
    tmp_path, monkeypatch, fake_embeddings
):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        policy_rag,
        "HuggingFaceEmbeddings",
        lambda **kwargs: fake_embeddings,
    )

    chunks = [
        Document(
            page_content=f"Test policy chunk {i}",
            metadata={"section_type": "active"},
        )
        for i in range(3)
    ]

    first_store = policy_rag.ingest_policy(chunks, "test_payer")
    assert first_store._collection.count() == 3

    second_store = policy_rag.ingest_policy(chunks, "test_payer")
    assert second_store._collection.count() == 3
