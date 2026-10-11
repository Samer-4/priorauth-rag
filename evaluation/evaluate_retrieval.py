import json
from datetime import datetime, timezone
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BASE_DIR = Path(__file__).resolve().parent.parent
QUERIES_FILE = BASE_DIR / "evaluation" / "retrieval_queries.json"
RESULTS_DIR = BASE_DIR / "evaluation" / "results"
DATABASE_DIR = BASE_DIR / "data" / "chroma_db"

MODEL_NAME = "ethanteh/bge-finetuned-insurance-matryoshka"
K = 5


def matches_expected(metadata: dict, expected: dict) -> bool:
    """Check whether a chunk belongs to the expected policy pathway."""

    if metadata.get("section_type") != "active":
        return False

    for key, value in expected.items():
        if key.endswith("_contains"):
            field = key.removesuffix("_contains")

            if value.lower() not in metadata.get(field, "").lower():
                return False
        else:
            if metadata.get(key, "").lower() != value.lower():
                return False

    return True


def evaluate_query(case: dict, vector_store: Chroma) -> dict:
    """Evaluate retrieval against pathway metadata labels."""

    expected = case["expected"]

    # Identify all indexed chunks matching the expected pathway.
    collection_data = vector_store.get(
        where={"section_type": "active"},
        include=["metadatas"],
    )

    relevant_ids = {
        chunk_id
        for chunk_id, metadata in zip(
            collection_data["ids"],
            collection_data["metadatas"],
        )
        if matches_expected(metadata or {}, expected)
    }

    if not relevant_ids:
        raise ValueError(
            f"{case['id']}: No chunks match expected metadata: {expected}. "
            "Check the labels and chunker before evaluating."
        )

    # Run semantic search across all active chunks, without
    # prefiltering by the expected answer.
    results = vector_store.similarity_search_with_score(
        query=case["query"],
        k=K,
        filter={"section_type": "active"},
    )

    ranked_results = []
    relevant_retrieved = 0

    for rank, (document, distance) in enumerate(results, start=1):
        is_relevant = matches_expected(document.metadata, expected)

        if is_relevant:
            relevant_retrieved += 1

        ranked_results.append({
            "rank": rank,
            "distance": round(float(distance), 4),
            "relevant": is_relevant,
            "section": document.metadata.get("section", ""),
            "medication": document.metadata.get("medication", ""),
            "indication": document.metadata.get("indication", ""),
            "pathway": document.metadata.get("pathway", ""),
            "text_preview": document.page_content[:250],
        })

    return {
        "id": case["id"],
        "payer": case["payer"],
        "query": case["query"],
        "expected": expected,
        "relevant_chunks_in_index": len(relevant_ids),
        "relevant_retrieved": relevant_retrieved,
        "retrieved_count": len(results),
        "hit_at_5": relevant_retrieved > 0,
        "precision_at_5": round(relevant_retrieved / K, 4),
        "recall_at_5": round(
            relevant_retrieved / len(relevant_ids), 4
        ),
        "results": ranked_results,
    }


def main():
    cases = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))

    if not DATABASE_DIR.exists():
        raise FileNotFoundError(f"ChromaDB not found: {DATABASE_DIR}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading embedding model: {MODEL_NAME}")

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"},
    )

    vector_stores = {}
    all_results = []

    for case in cases:
        payer = case["payer"]

        if payer not in vector_stores:
            vector_stores[payer] = Chroma(
                collection_name=f"{payer}_policy",
                embedding_function=embeddings,
                persist_directory=str(DATABASE_DIR),
            )

            count = vector_stores[payer]._collection.count()
            print(f"{payer.upper()}: {count} indexed chunks")

            if count == 0:
                raise ValueError(f"No indexed chunks for {payer}")

        result = evaluate_query(case, vector_stores[payer])
        all_results.append(result)

        print(
            f"{result['id']}: "
            f"Hit@5={result['hit_at_5']} | "
            f"Precision@5={result['precision_at_5']:.2f} | "
            f"Recall@5={result['recall_at_5']:.2f}"
        )

    count = len(all_results)

    summary = {
        "queries": count,
        "hit_rate_at_5": round(
            sum(r["hit_at_5"] for r in all_results) / count, 4
        ),
        "mean_precision_at_5": round(
            sum(r["precision_at_5"] for r in all_results) / count, 4
        ),
        "mean_recall_at_5": round(
            sum(r["recall_at_5"] for r in all_results) / count, 4
        ),
    }

    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "embedding_model": MODEL_NAME,
        "k": K,
        "evaluation_type": "metadata_labeled_pathway_retrieval",
        "note": (
            "Relevance labels are derived from existing section metadata. "
            "They are not independently verified clinical gold labels. "
            "Requirement completeness is not measured."
        ),
        "summary": summary,
        "queries": all_results,
    }

    output_json = RESULTS_DIR / "retrieval_evaluation.json"
    output_txt = RESULTS_DIR / "retrieval_evaluation.txt"

    output_json.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "RAG RETRIEVAL EVALUATION",
        f"Embedding model: {MODEL_NAME}",
        f"Queries: {count}",
        f"Hit Rate@5: {summary['hit_rate_at_5']:.2%}",
        f"Mean Precision@5: {summary['mean_precision_at_5']:.2%}",
        f"Mean Recall@5: {summary['mean_recall_at_5']:.2%}",
        "",
        "These metrics use metadata-based pathway relevance labels.",
        "They do not measure clinical requirement completeness.",
        "",
    ]

    for result in all_results:
        lines.append(
            f"{result['id']} | "
            f"Hit@5={result['hit_at_5']} | "
            f"Precision@5={result['precision_at_5']:.2f} | "
            f"Recall@5={result['recall_at_5']:.2f}"
        )

        for chunk in result["results"]:
            lines.append(
                f"  Rank {chunk['rank']}: "
                f"distance={chunk['distance']:.4f} | "
                f"relevant={chunk['relevant']} | "
                f"{chunk['section']} | "
                f"{chunk['medication']} | "
                f"{chunk['indication']} | "
                f"{chunk['pathway']}"
            )

        lines.append("")

    output_txt.write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "=" * 50)
    print("RETRIEVAL EVALUATION SUMMARY")
    print("=" * 50)
    print(f"Queries: {count}")
    print(f"Hit Rate@5: {summary['hit_rate_at_5']:.2%}")
    print(f"Mean Precision@5: {summary['mean_precision_at_5']:.2%}")
    print(f"Mean Recall@5: {summary['mean_recall_at_5']:.2%}")
    print(f"\nSaved JSON: {output_json}")
    print(f"Saved text: {output_txt}")


if __name__ == "__main__":
    main()
