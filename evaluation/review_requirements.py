import json
from datetime import datetime, timezone
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "data/chroma_db"
QUERIES_FILE = BASE_DIR / "evaluation/retrieval_queries.json"
OUTPUT_FILE = BASE_DIR / "evaluation/results/requirement_review.md"

MODEL_NAME = "ethanteh/bge-finetuned-insurance-matryoshka"

COLLECTIONS = {
    "aetna": "aetna_policy_context_v2",
    "cigna": "cigna_policy_context_v2",
    "unitedhealthcare": "unitedhealthcare_policy_context_v2",
}


def main():
    cases = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"},
    )

    vector_stores = {}
    lines = [
        "# Prior Authorization RAG — Requirement Review",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Embedding model: {MODEL_NAME}",
        "Retrieval: contextual V2, top 5 active chunks per payer",
        "",
        "## Review instructions",
        "",
        "For each query, verify against the original policy:",
        "",
        "- [ ] Correct medication and indication",
        "- [ ] Correct authorization pathway",
        "- [ ] All mandatory requirements are present",
        "- [ ] Nested AND/OR conditions are preserved",
        "- [ ] No incorrect or historical requirements included",
        "",
        "Do not treat an unchecked item as passed.",
        "This report is a review worksheet, not a clinical accuracy score.",
        "",
    ]

    for case in cases:
        payer = case["payer"]

        if payer not in vector_stores:
            store = Chroma(
                collection_name=COLLECTIONS[payer],
                embedding_function=embeddings,
                persist_directory=str(DATABASE_DIR),
            )

            if store._collection.count() == 0:
                raise ValueError(f"Empty collection for {payer}")

            vector_stores[payer] = store

        results = vector_stores[payer].similarity_search_with_score(
            query=case["query"],
            k=5,
            filter={"section_type": "active"},
        )

        lines.extend([
            "",
            "---",
            "",
            f"## {case['id']}",
            "",
            f"**Payer:** {payer}",
            "",
            f"**Query:** {case['query']}",
            "",
            f"**Expected pathway metadata:** `{json.dumps(case['expected'])}`",
            "",
            "### Mandatory requirements — manual ground truth",
            "",
            "- [ ] Review original policy and list every required condition here",
            "",
            "### Retrieval review",
            "",
            "- [ ] Correct pathway retrieved",
            "- [ ] All mandatory conditions covered",
            "- [ ] AND/OR logic preserved",
            "",
        ])

        for rank, (document, distance) in enumerate(results, start=1):
            metadata = document.metadata

            if "original_text" not in metadata:
                raise ValueError(
                    f"{case['id']}, rank {rank}: original_text missing"
                )

            original_text = metadata["original_text"]

            lines.extend([
                f"### Rank {rank} — Distance {distance:.4f}",
                "",
                f"- Section: {metadata.get('section', '')}",
                f"- Medication: {metadata.get('medication', '')}",
                f"- Indication: {metadata.get('indication', '')}",
                f"- Pathway: {metadata.get('pathway', '')}",
                "",
                "**Original policy text:**",
                "",
                "```text",
                original_text,
                "```",
                "",
            ])

        print(
            f"{case['id']}: {len(results)} chunks retrieved "
            f"from {COLLECTIONS[payer]}"
        )

    OUTPUT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"\nSaved review worksheet: {OUTPUT_FILE}")
    print(f"Queries prepared for review: {len(cases)}")


if __name__ == "__main__":
    main()
