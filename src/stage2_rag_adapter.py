"""Opt-in Stage 2 RAG adapter.

Does not change the existing Stage 2 implementation.
"""

import sys
from pathlib import Path

from src.policy_context_retrieval import retrieve_policy_context


def extract_criteria_with_rag(
    denial_info,
    *,
    medication: str,
    indication: str,
    pathway: str,
    scope: str | None = None,
):
    """Retrieve verified pathway text, then call existing Stage 2."""

    context = retrieve_policy_context(
        payer=denial_info.payer,
        medication=medication,
        indication=indication,
        pathway=pathway,
        scope=scope,
    )

    # Existing stage files use local imports such as
    # `from stage1_extraction import ...`.
    src_dir = str(Path(__file__).resolve().parent)

    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    from stage2_lookup import extract_criteria

    return extract_criteria(context.policy_text, denial_info)
