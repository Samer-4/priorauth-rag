import json
from datetime import datetime, timezone
from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from src.policy_rag import chunk_policy
from evaluation.evaluate_retrieval import evaluate_query


BASE_DIR = Path(__file__).resolve().parent.parent
POLICY_FILE = BASE_DIR / "data/policies/policies_txt/cigna_glp1_prior_auth.txt"
DATABASE_DIR = BASE_DIR / "data/chroma_db"
QUERIES_FILE = BASE_DIR / "evaluation/retrieval_queries.json"
RESULTS_DIR = BASE_DIR / "evaluation/results"
BASELINE_FILE = RESULTS_DIR / "retrieval_evaluation.json"

MODEL_NAME = "ethanteh/bge-finetuned-insurance-matryoshka"
COLLECTION_NAME = "cigna_policy_context_v2"


def add_context(chunks: list[Document]) -> list[Document]:
    """Add policy context for embeddings while preserving original text."""

    contextual_chunks = []

    for source_index, chunk in enumerate(chunks):
        metadata = chunk.metadata.copy()
        metadata["source_chunk_index"] = source_index

        original_text = chunk.page_content

        context = [
            "Insurance provider: Cigna",
            f"Section: {metadata.get('section', '')}",
            f"Medication: {metadata.get('medication', '')}",
            f"Indication: {metadata.get('indication', '')}",
            f"Authorization pathway: {metadata.get('pathway', '')}",
        ]

        contextual_text = (
            "\n".join(context)
            + "\n\n"
            + original_text
        )

        metadata["payer"] = "cigna"
        metadata["original_text"] = original_text

        contextual_chunks.append(
            Document(
                page_content=contextual_text,
                metadata=metadata,
            )
        )

    return contextual_chunks


def ranking_metrics(result: dict) -> dict:
    """Calculate ranking metrics from retrieved relevance labels."""

    relevant_ranks = [
        chunk["rank"]
        for chunk in result["results"]
        if chunk["relevant"]
    ]

    mrr = 1 / relevant_ranks[0] if relevant_ranks else 0.0

    relevant_found = 0
    precision_sum = 0.0

    for chunk in result["results"]:
        if chunk["relevant"]:
            relevant_found += 1
            precision_sum += relevant_found / chunk["rank"]

    denominator = min(result["relevant_chunks_in_index"], 5)
    ap_at_5 = precision_sum / denominator if denominator else 0.0

    return {
        "mrr_at_5": round(mrr, 4),
        "ap_at_5": round(ap_at_5, 4),
    }


def summarize(results: list[dict]) -> dict:
    """Calculate averages across evaluation queries."""

    count = len(results)

    return {
        "queries": count,
        "hit_rate_at_5": round(
            sum(result["hit_at_5"] for result in results) / count, 4
        ),
        "mean_precision_at_5": round(
            sum(result["precision_at_5"] for result in results) / count, 4
        ),
        "mean_recall_at_5": round(
            sum(result["recall_at_5"] for result in results) / count, 4
        ),
        "mrr_at_5": round(
            sum(result["ranking"]["mrr_at_5"] for result in results) / count, 4
        ),
        "map_at_5": round(
            sum(result["ranking"]["ap_at_5"] for result in results) / count, 4
        ),
    }


def main():
    if not BASELINE_FILE.exists():
        raise FileNotFoundError(
            "Run the original retrieval benchmark first."
        )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    cases = json.loads(
        QUERIES_FILE.read_text(encoding="utf-8")
    )

    cigna_cases = [
        case for case in cases
        if case["payer"] == "cigna"
    ]

    baseline_report = json.loads(
        BASELINE_FILE.read_text(encoding="utf-8")
    )

    baseline_results = [
        result for result in baseline_report["queries"]
        if result["payer"] == "cigna"
    ]

    baseline_ids = {result["id"] for result in baseline_results}
    current_ids = {case["id"] for case in cigna_cases}

    if baseline_ids != current_ids:
        raise ValueError(
            "Baseline and experiment query IDs do not match."
        )

    print("Loading original Cigna policy...")

    policy_text = POLICY_FILE.read_text(encoding="utf-8")
    original_chunks = chunk_policy(policy_text)

    contextual_chunks = add_context(original_chunks)

    assert len(contextual_chunks) == len(original_chunks)

    for original, contextual in zip(original_chunks, contextual_chunks):
        assert contextual.metadata["original_text"] == original.page_content

    print(f"Original chunks: {len(original_chunks)}")
    print(f"Contextual chunks: {len(contextual_chunks)}")

    print(f"\nLoading embedding model: {MODEL_NAME}")

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"},
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(DATABASE_DIR),
    )

    # Reset only the experimental collection.
    # Original Cigna, Aetna, and UHC indexes remain untouched.
    vector_store.reset_collection()
    vector_store.add_documents(contextual_chunks)

    stored_count = vector_store._collection.count()

    print(f"\nExperimental collection: {COLLECTION_NAME}")
    print(f"Expected chunks: {len(contextual_chunks)}")
    print(f"Stored records: {stored_count}")

    assert stored_count == len(contextual_chunks)

    print("\nRunning the same five Cigna queries...")

    experiment_results = []

    for case in cigna_cases:
        result = evaluate_query(case, vector_store)
        result["ranking"] = ranking_metrics(result)
        experiment_results.append(result)

        print(
            f"{result['id']}: "
            f"Hit@5={result['hit_at_5']} | "
            f"Recall@5={result['recall_at_5']:.2f} | "
            f"MRR@5={result['ranking']['mrr_at_5']:.2f} | "
            f"AP@5={result['ranking']['ap_at_5']:.2f}"
        )

    for result in baseline_results:
        result["ranking"] = ranking_metrics(result)

    baseline_summary = summarize(baseline_results)
    experiment_summary = summarize(experiment_results)

    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "experiment": "Cigna contextual embeddings V2",
        "embedding_model": MODEL_NAME,
        "baseline_collection": "cigna_policy",
        "experiment_collection": COLLECTION_NAME,
        "description": (
            "Same chunker, embedding model, queries, and K=5. "
            "V2 prefixes medication, indication, section, and pathway "
            "context to the embedded text."
        ),
        "limitations": (
            "Relevance labels are based on existing chunk metadata, "
            "not independently validated clinical requirements. "
            "Metadata errors and incomplete criteria remain possible."
        ),
        "baseline": baseline_summary,
        "contextual_v2": experiment_summary,
        "baseline_queries": baseline_results,
        "experiment_queries": experiment_results,
    }

    output_file = RESULTS_DIR / "contextual_cigna_comparison.json"

    output_file.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    print("CIGNA RETRIEVAL COMPARISON: V1 VS V2")
    print("=" * 60)

    print(f"{'Metric':<22} {'Baseline V1':>14} {'Context V2':>14}")

    metrics = [
        ("Hit Rate@5", "hit_rate_at_5"),
        ("Mean Precision@5", "mean_precision_at_5"),
        ("Mean Recall@5", "mean_recall_at_5"),
        ("MRR@5", "mrr_at_5"),
        ("MAP@5", "map_at_5"),
    ]

    for label, key in metrics:
        print(
            f"{label:<22} "
            f"{baseline_summary[key]:>14.2%} "
            f"{experiment_summary[key]:>14.2%}"
        )

    print(f"\nSaved comparison: {output_file}")
    print("Original indexes and baseline results were not overwritten.")


if __name__ == "__main__":
    main()
