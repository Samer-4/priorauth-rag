from stage1_extraction import extract_denial_info
from stage2_lookup import extract_criteria, policy_files
from stage3_evidence_extraction import notes_extraction, CriterionEvidence, NoteEvidence
from llm_client import get_client
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
from typing import Literal
from datetime import datetime

load_dotenv()
client = get_client()

BASE_DIR = Path(__file__).resolve().parent.parent

class ComponentJudgment(BaseModel):
    component: str
    status: Literal["satisfied", "not_satisfied"]

class SufficiencyJudgment(BaseModel):
    criterion_name: str
    requirement: str
    evidence: list[NoteEvidence]
    status: Literal["satisfied", "partial", "not_satisfied"]
    components: list[ComponentJudgment]
    reasoning: str
    missing: list[str]
    date_start: str | None = None
    date_end: str | None = None
    computed_span_months: float | None = None

class JudgmentResult(BaseModel):
    status: Literal["satisfied", "partial", "not_satisfied"]
    components: list[ComponentJudgment]
    reasoning: str
    missing: list[str]
    date_start: str | None = None
    date_end: str | None = None

def sufficiency_judgment(evidence_results: list[CriterionEvidence]) -> list[SufficiencyJudgment]:
    sufficiency_results = []
    for evidence_result in evidence_results:
        if not evidence_result.criterion_name or not evidence_result.requirement:
            raise ValueError(f"Criterion object is missing required fields: {evidence_result}")
        if not evidence_result.evidence:
            sufficiency_results.append(SufficiencyJudgment(
                criterion_name=evidence_result.criterion_name,
                requirement=evidence_result.requirement,
                evidence=[],
                status="not_satisfied",
                components=[],
                reasoning="No relevant evidence was found in the clinical notes.",
                missing=[evidence_result.requirement]
            ))
            continue
        
        resp = client.messages.parse(
            model = "claude-sonnet-5",
            max_tokens = 3000,
            messages=[
                {
                "role": "user",
                "content": f"""
                You are evaluating whether clinical evidence satisfies a specific prior-authorization policy requirement.

                POLICY REQUIREMENT:
                {evidence_result.requirement}

                EXTRACTED CLINICAL EVIDENCE:
                {evidence_result.evidence}

                Determine whether the provided evidence satisfies the policy requirement.

                Rules:
                - Judge ONLY from the extracted clinical evidence provided above.
                - Do not assume, infer, or invent clinical facts that are not explicitly supported by the evidence.
                - Do not search for or introduce additional evidence.
                - Do not treat missing information as evidence that something occurred.

                - If the policy requirement is a simple single-part requirement, evaluate it directly and return `components` as an empty list.

                - If the policy requirement contains multiple distinct components that must all be met, evaluate each component separately and include each one in `components`.
                - Do not create unnecessary components for simple requirements.
                - For each component, determine whether it is "satisfied" or "not_satisfied" based only on the provided evidence.

                Overall status rules:
                - "satisfied" means every required component is supported by the evidence.
                - "partial" means at least one required component is supported, but one or more other required components are not supported.
                - "not_satisfied" means none of the required components are supported, the evidence explicitly contradicts the requirement, or there is no relevant evidence.

                Additional rules:
                - Keep the overall reasoning concise and explain why the overall status was assigned.
                - In `missing`, list only the specific required components or information that are not supported by the evidence.
                - If the requirement is fully satisfied, return an empty `missing` list.
                - If the policy requirement depends on a duration or time span, populate `date_start` and `date_end` using only dates explicitly supported by the provided evidence.
                - `date_start` should be the relevant beginning date used to evaluate the duration requirement.
                - `date_end` should be the relevant endpoint used to evaluate the duration requirement.
                - If the requirement does not involve a duration, return `date_start` and `date_end` as null.
                - Return `date_start` and `date_end` in YYYY-MM-DD format.
                """
                }
            ],
            output_format=JudgmentResult,
        )

        date_start = resp.parsed_output.date_start
        date_end = resp.parsed_output.date_end

        computed_span_months = None

        if date_start and date_end:
            start = datetime.strptime(date_start, "%Y-%m-%d")
            end = datetime.strptime(date_end, "%Y-%m-%d")
            days = (end - start).days
            computed_span_months = round(days / 30.44, 2)

        sufficiency_results.append(SufficiencyJudgment(
            criterion_name=evidence_result.criterion_name,
            requirement=evidence_result.requirement,
            evidence=evidence_result.evidence,
            status=resp.parsed_output.status,
            components=resp.parsed_output.components,
            reasoning=resp.parsed_output.reasoning,
            missing=resp.parsed_output.missing,
            date_start=resp.parsed_output.date_start,
            date_end=resp.parsed_output.date_end,
            computed_span_months=computed_span_months
        ))
    return sufficiency_results

if __name__ == "__main__":
    file_path = BASE_DIR / "data" / "cases" / "cases_v1" / "denial_letters" / "case_001_denial.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        text_data = f.read()
    denial_info = extract_denial_info(text_data)
    payer = denial_info.payer.lower()
    policy_file_path = policy_files.get(payer)
    if policy_file_path:
        with open(policy_file_path, "r", encoding="utf-8") as f:
            policy_text = f.read()
    else:
        raise ValueError(f"No policy file found for payer: {denial_info.payer}")
    criteria = extract_criteria(policy_text, denial_info)
    notes_file_path = BASE_DIR / "data" / "cases" / "cases_v1" / "notes" / "case_001_note.txt"
    with open(notes_file_path, "r", encoding="utf-8") as f:
        notes_text = f.read()
    evidence_results = notes_extraction(notes_text, criteria)
    sufficiency_results = sufficiency_judgment(evidence_results)
    print(sufficiency_results)