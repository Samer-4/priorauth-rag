#!/usr/bin/env bash
# HTTP smoke tests against the saved-results API container.
# Usage: scripts/docker_smoke_test.sh [image] [host_port]
set -euo pipefail

IMAGE="${1:-priorauth-api}"
PORT="${2:-8000}"
BASE_URL="http://127.0.0.1:${PORT}"
CONTAINER="priorauth-api-smoke-$$"

cleanup() {
    if [ "$status" -ne 0 ]; then
        echo "--- container logs ---"
        docker logs "$CONTAINER" 2>&1 || true
    fi
    docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
}
status=1
trap cleanup EXIT

docker run -d --name "$CONTAINER" -p "${PORT}:8000" "$IMAGE" >/dev/null

# Wait up to 30s for the server to accept requests
for _ in $(seq 1 30); do
    if curl -fsS "${BASE_URL}/health" >/dev/null 2>&1; then
        break
    fi
    sleep 1
done

# Fetch a URL, require the expected HTTP status, and check the JSON body
# with a Python expression evaluated against `body`.
check() {
    local path="$1" expected_status="$2" assertion="$3"
    local response http_status body
    response="$(curl -sS -w '\n%{http_code}' "${BASE_URL}${path}")"
    http_status="${response##*$'\n'}"
    body="${response%$'\n'*}"

    if [ "$http_status" != "$expected_status" ]; then
        echo "FAIL ${path}: expected HTTP ${expected_status}, got ${http_status}"
        return 1
    fi
    if ! BODY="$body" python3 -c \
        "import json, os, sys; body = json.loads(os.environ['BODY']); sys.exit(0 if (${assertion}) else 1)"; then
        echo "FAIL ${path}: assertion failed: ${assertion}"
        return 1
    fi
    echo "PASS ${path} (${http_status})"
}

check "/health" 200 "body == {'status': 'healthy'}"
check "/cases" 200 "isinstance(body, list) and len(body) == 30"
check "/cases/001" 200 "body['case'] == 'case_001'"
check "/cases/001/findings" 200 "len(body) == 3 and body[0]['check_name'] == 'stage4_consistency'"
check "/cases/009/findings" 200 "body == []"
check "/cases/999" 404 "body['detail'] == 'Case not found'"

status=0
echo "All smoke tests passed."
