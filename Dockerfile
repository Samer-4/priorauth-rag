# Saved-results API image. Serves benchmark JSON only; no model inference.
# Base images are pinned by multi-arch digest (amd64 + arm64).
FROM ghcr.io/astral-sh/uv:0.11.18@sha256:78bc42400d77b0678ba95765305c826652ed5431f399257271dda681d0318f03 AS uv

# python:3.12-slim (Python 3.12.15)
FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1

COPY --from=uv /uv /usr/local/bin/uv

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/app/.venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1

# Install only the "api" dependency group at the versions pinned in uv.lock.
# --locked fails the build if uv.lock is out of date with pyproject.toml.
COPY pyproject.toml uv.lock /app/
RUN uv sync --locked --only-group api

ENV PATH="/app/.venv/bin:$PATH"

COPY src/api.py /app/src/api.py

COPY evaluation/results/qwen35_30_case_batch/*.json /app/evaluation/results/qwen35_30_case_batch/

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
