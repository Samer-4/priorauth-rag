import hashlib

import pytest
from langchain_core.embeddings import Embeddings


class TestEmbeddings(Embeddings):
    """Deterministic embeddings for fast, offline software tests."""

    def embed_documents(self, texts):
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text):
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        return [float(value) / 255 for value in digest]


@pytest.fixture
def fake_embeddings():
    return TestEmbeddings()
