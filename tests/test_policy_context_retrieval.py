"""Fast regression tests with no model download or LLM calls."""

from types import SimpleNamespace

import pytest

from src import policy_context_retrieval as rag


class FakeCollection:
    def count(self):
        return 1


class FakeStore:
    _collection = FakeCollection()

    def __init__(self, metadata, original):
        self.metadata = metadata
        self.original = original

    def get(self, *, where, include):
        assert where == {"section_type": "active"}

        return {
            "ids": ["test-chunk"],
            "metadatas": [self.metadata],
            "documents": [
                "Insurance provider: Test\n\n" + self.original
            ],
        }


def test_unsupported_payer_rejected():
    with pytest.raises(rag.PolicyRetrievalError):
        rag.retrieve_policy_context(
            payer="unknown",
            medication="Wegovy",
            indication="adult weight loss",
            pathway="initial",
        )


def test_missing_uhc_scope_rejected():
    with pytest.raises(rag.PolicyRetrievalError, match="scope"):
        rag.retrieve_policy_context(
            payer="unitedhealthcare",
            medication="Wegovy",
            indication="weight loss",
            pathway="initial",
        )


def test_invalid_pathway_rejected():
    with pytest.raises(rag.PolicyRetrievalError):
        rag.retrieve_policy_context(
            payer="aetna",
            medication="Wegovy",
            indication="Chronic Weight Management (Adult)",
            pathway="unknown",
        )


def test_cigna_original_text_only(monkeypatch):
    original = (
        "A) Initial Therapy. Patient is at least 18 years old."
    )

    metadata = {
        "section_type": "active",
        "medication": "Wegovy injection",
        "indication": "Weight Loss in an Adult",
        "pathway": "A) Initial Therapy.",
        "original_text": original,
    }

    monkeypatch.setattr(
        rag, "_store", lambda payer: FakeStore(metadata, original)
    )

    result = rag.retrieve_policy_context(
        payer="cigna",
        medication="Wegovy injection",
        indication="Weight Loss in an Adult",
        pathway="initial",
    )

    assert result.policy_text == original
    assert "Insurance provider: Test" not in result.policy_text


def test_wrong_uhc_scope_rejected(monkeypatch):
    original = "A. Initial Authorization"

    metadata = {
        "section_type": "active",
        "scope": "general",
        "pathway": "Initial Authorization",
        "original_text": original,
    }

    monkeypatch.setattr(
        rag, "_store", lambda payer: FakeStore(metadata, original)
    )

    with pytest.raises(rag.PolicyRetrievalError, match="No chunks"):
        rag.retrieve_policy_context(
            payer="unitedhealthcare",
            medication="Wegovy",
            indication="weight loss",
            pathway="initial",
            scope="north_dakota",
        )
