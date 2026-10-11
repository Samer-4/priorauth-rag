import json
from datetime import datetime, timezone
from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from src.policy_rag import chunk_policy
from evaluation.evaluate_retrieval import evaluate_query
from evaluation.experiment_contextual_cigna import ranking_metrics, summarize


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "data/chroma_db"
RESULTS_DIR = BASE_DIR / "evaluation/results"
QUERIES_FILE = BASE_DIR / "evaluation/retrieval_queries.json"
BASELINE_FILE = RESULTS_DIR / "retrieval_evaluation.json"

MODEL_NAME = "ethanteh/bge-finetuned-insurance-matryoshka"

POLICIES = {
    "aetna": BASE_DIR / "data/policies/policies_txt/aetna_glp1_weight_management.txt",
    "unitedhealthcare": BASE_DIR / "data/policies/policies_txt/uhc_weight_loss_prior_auth.txt",
}


def add_context(chunks: list[Document], payer: str) -> list[Document]:
    """Add section context to embeddings while retaining original text."""

    contextual_chunks = []

    for chunk in chunks:
        metadata = chunk.metadata.copy()
        original_text = chunk.page_content

        context = [
            f"Insurance provider: {payer}",
            f"Section: {metadata.get('section', '')}",
            f"Medication: {metadata.get('medication', '')}",
            f"Indication: {metadata.get('indication', '')}",
            f"Authorization pathway: {metadata.get('pathway', '')}",
        ]

        contextual_text = "\n".join(context) + "\n\n" + original_text

        metadata["payer"] = payer
        metadata["original_text"] = original_text

        contextual_chunks.append(
            Document(
                page_content=contextual_text,
                metadata=metadata,
            )
        )

    return contextual_chunks


def main():
    if not BASELINE_FILE.exists():
        raise FileNotFoundError("Original retrieval benchmark not found.")

    cases = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"},
    )

    comparisons = {}

    for payer, policy_file in POLICIES.items():
        print(f"\n{'=' * 60}")
        print(f"PROCESSING {payer.upper()}")
        print("=" * 60)

        policy_text = policy_file.read_text(encoding="utf-8")

        original_chunks = chunk_policy(policy_text)
        contextual_chunks = add_context(original_chunks, payer)

        for original, contextual in zip(original_chunks, contextual_chunks):
            assert contextual.metadata["original_text"] == original.page_content

        collection_name = f"{payer}_policy_context_v2"

        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=str(DATABASE_DIR),
        )

        # Reset only the experimental collection.
        vector_store.reset_collection()
        vector_store.add_documents(contextual_chunks)

        stored_count = vector_store._collection.count()

        print(f"Collection: {collection_name}")
        print(f"Expected chunks: {len(contextual_chunks)}")
        print(f"Stored chunks: {stored_count}")

        assert stored_count == len(contextual_chunks)

        payer_cases = [
            case for case in cases
            if case["payer"] == payer
        ]

        baseline_results = [
            result for result in baseline["queries"]
            if result["payer"] == payer
        ]

        if {c["id"] for c in payer_cases} != {
            r["id"] for r in baseline_results
        }:
            raise ValueError(f"Baseline query mismatch for {payer}")

        experiment_results = []

        for case in payer_cases:
            result = evaluate_query(case, vector_store)
            result["ranking"] = ranking_metrics(result)
            experiment_results.append(result)

            print(
                f"{result['id']}: "
                f"Hit@5={result['hit_at_5']} | "
                f"Recall@5={result['recall_at_5']:.2f} | "
                f"MRR@5={result['ranking']['mrr_at_5']:.2f}"
            )

        for result in baseline_results:
            result["ranking"] = ranking_metrics(result)

        baseline_summary = summarize(baseline_results)
        experiment_summary = summarize(experiment_results)

        comparisons[payer] = {
            "baseline": baseline_summary,
            "contextual_v2": experiment_summary,
            "baseline_queries": baseline_results,
            "experiment_queries": experiment_results,
            "collection": collection_name,
            "stored_chunks": stored_count,
        }

        print(f"\n{payer.upper()} — V1 VS V2")
        print(f"{'Metric':<22} {'V1':>12} {'V2':>12}")

        metrics = [
            ("Hit Rate@5", "hit_rate_at_5"),
            ("Precision@5", "mean_precision_at_5"),
            ("Recall@5", "mean_recall_at_5"),
            ("MRR@5", "mrr_at_5"),
            ("MAP@5", "map_at_5"),
        ]

        for label, key in metrics:
            print(
                f"{label:<22} "
                f"{baseline_summary[key]:>12.2%} "
                f"{experiment_summary[key]:>12.2%}"
            )

    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "embedding_model": MODEL_NAME,
        "experiment": "Contextual Embeddings V2 - Aetna and UHC",
        "k": 5,
        "note": (
            "Relevance labels are based on the existing section metadata. "
            "This benchmark does not independently verify clinical "
            "criteria completeness or metadata correctness."
        ),
        "comparisons": comparisons,
    }

    output_path = RESULTS_DIR / "contextual_remaining_comparison.json"

    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    print("EXPERIMENT COMPLETE")
    print("=" * 60)
    print(f"Saved results: {output_path}")
    print("Original payer collections remain unchanged.")


if __name__ == "__main__":
    main()
