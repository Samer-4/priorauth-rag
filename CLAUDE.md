
# Prior Authorization Appeal Generator

## Project overview
Six-stage healthcare AI pipeline that generates
evidence-grounded draft appeals for human review.

Current architecture:
- Python pipeline with Qwen LLM inference
- LangChain and ChromaDB policy retrieval
- Pydantic structured outputs
- FastAPI read-only benchmark results API
- Docker container for the API
- Pytest API regression tests

## Engineering rules
1. Inspect relevant code before making changes.
2. For nontrivial changes, present a short implementation plan.
3. Make minimal, focused modifications.
4. Do not refactor unrelated code.
5. Preserve the existing six-stage pipeline unless explicitly asked.
6. Never invent patient facts or policy citations.
7. Never automatically submit clinical appeals.
8. Keep synthetic test data separate from real PHI.
9. Add or update tests for changes in behavior.
10. Do not claim tests passed unless actually executed.
11. Never commit secrets, credentials, or real PHI.
12. Do not commit or push without approval.

## Development workflow
- Use uv for dependency management.
- Run API tests with:
  uv run python -m pytest tests/test_api.py -v
- Validate Docker builds with:
  docker build -t priorauth-api .
  scripts/docker_smoke_test.sh priorauth-api 8000
- CI (.github/workflows/api-ci.yml) installs only the
  `api-test` uv group and runs pytest with --noconftest,
  because tests/conftest.py imports langchain_core.
- Review git diff before finalizing changes.

## Learning requirements
After implementation:
- Summarize modified files and why.
- Explain the execution flow.
- Explain significant design decisions.
- Identify failure modes and debugging steps.
- Report tests executed and results.
- Ask one technical comprehension question.

## Current priority
Implement GitHub Actions CI for the saved-results
FastAPI backend without running live Qwen inference.
