import json
from pathlib import Path

import pytest

from evaluation.evaluate_retrieval import matches_expected


def test_retrieval_dataset_has_unique_queries():
    path = Path("evaluation/retrieval_queries.json")
    cases = json.loads(path.read_text(encoding="utf-8"))

    ids = [case["id"] for case in cases]

    assert len(cases) >= 10
    assert len(ids) == len(set(ids))


def test_retrieval_dataset_has_required_fields():
    path = Path("evaluation/retrieval_queries.json")
    cases = json.loads(path.read_text(encoding="utf-8"))

    for case in cases:
        assert case["id"]
        assert case["payer"] in {
            "aetna", "cigna", "unitedhealthcare"
        }
        assert case["query"]
        assert case["expected"]


def test_metadata_matching():
    metadata = {
        "section_type": "active",
        "section": "COVERAGE CRITERIA",
        "indication": "Chronic Weight Management (Adult)",
    }

    expected = {
        "section": "COVERAGE CRITERIA",
        "indication_contains": "Weight Management (Adult)",
    }

    assert matches_expected(metadata, expected)


def test_history_not_relevant():
    metadata = {
        "section_type": "history",
        "section": "COVERAGE CRITERIA",
    }

    assert not matches_expected(
        metadata, {"section": "COVERAGE CRITERIA"}
    )


def test_evaluation_report_integrity():
    path = Path("evaluation/results/retrieval_evaluation.json")

    if not path.exists():
        pytest.skip("Run retrieval evaluation first")

    report = json.loads(path.read_text(encoding="utf-8"))

    assert report["summary"]["queries"] == len(report["queries"])

    for result in report["queries"]:
        assert result["relevant_chunks_in_index"] > 0
        assert 0 <= result["precision_at_5"] <= 1
        assert 0 <= result["recall_at_5"] <= 1
        assert result["relevant_retrieved"] <= result["retrieved_count"]
        assert result["retrieved_count"] <= report["k"]
