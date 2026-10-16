
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Prior Authorization Appeal API")

# Locate benchmark results relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_PATH = BASE_DIR / "evaluation/results/qwen35_30_case_batch/summary.json"


# Define the response structure
class CaseResponse(BaseModel):
    case: str
    completed: bool
    findings: int
    error: str | None
    seconds: float

class VerificationFinding(BaseModel):
    check_name: str
    claim: str
    evidence_ids: list[str]
    reason: str


# Load saved benchmark results
def load_cases():
    with open(RESULTS_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["results"]


# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Return all 30 cases
@app.get("/cases", response_model=list[CaseResponse])
def get_cases():
    return load_cases()


# Return one specific case
@app.get("/cases/{case_id}", response_model=CaseResponse)
def get_case(case_id: str):
    cases = load_cases()

    # Accept both "001" and "case_001"
    normalized_id = (
        case_id if case_id.startswith("case_")
        else f"case_{case_id}"
    )

    for case in cases:
        if case["case"] == normalized_id:
            return case

    raise HTTPException(
        status_code=404,
        detail="Case not found"
    )


@app.get("/cases/{case_id}/findings", response_model=list[VerificationFinding])
def get_case_findings(case_id: str):
    normalized_id = (
        case_id if case_id.startswith("case_")
        else f"case_{case_id}"
    )

    # Verify that the case exists in the benchmark
    if not any(case["case"] == normalized_id for case in load_cases()):
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    checkpoint_path = RESULTS_PATH.parent / f"{normalized_id}.json"

    if not checkpoint_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Case checkpoint not found"
        )

    with checkpoint_path.open("r", encoding="utf-8") as file:
        checkpoint = json.load(file)

    return checkpoint["findings"]