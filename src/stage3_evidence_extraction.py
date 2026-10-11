from stage1_extraction import extract_denial_info
from stage2_lookup import extract_criteria, Criterion, policy_files
from llm_client import get_client
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import re

load_dotenv()
client = get_client()

BASE_DIR = Path(__file__).resolve().parent.parent

class NoteEvidence(BaseModel):
    evidence_id: str | None = None
    note_text: str
    line_start: int | None = None
    line_end: int | None = None

class CriterionEvidence(BaseModel):
    criterion_name: str
    requirement: str
    evidence: list[NoteEvidence]


class EvidenceRange(BaseModel):
    start: int
    end: int


class EvidenceRanges(BaseModel):
    ranges: list[EvidenceRange]

def find_quote_lines(notes: str, quote: str):
    def clean(text):
        return re.sub(r"\s+", " ", text).strip()

    lines = notes.splitlines()

    quote_parts = [
        clean(part)
        for part in quote.splitlines()
        if clean(part)
    ]

    if not quote_parts:
        return None, None

    first_part = quote_parts[0]
    last_part = quote_parts[-1]
    line_start = None

    for i, line in enumerate(lines):
        clean_line = clean(line)

        if first_part in clean_line:
            line_start = i + 1
            break

    if line_start is None:
        return None, None

    line_end = None

    for i in range(line_start - 1, len(lines)):
        clean_line = clean(lines[i])

        if last_part in clean_line:
            line_end = i + 1
            break

    if line_end is None:
        return None, None

    return line_start, line_end


def verify_quote_lines(notes: str, evidence: NoteEvidence) -> bool:
    if evidence.line_start is None or evidence.line_end is None:
        return False

    lines = notes.splitlines()

    source_text = "\n".join(
        lines[evidence.line_start - 1:evidence.line_end]
    )

    def clean(text):
        return re.sub(r"\s+", " ", text).strip()

    return clean(evidence.note_text) == clean(source_text)

        
def notes_extraction(notes: str, criteria: list[Criterion]) -> list[CriterionEvidence]:
    result = []
    evidence_ids = {}
    evidence_counter = 1

    lines = notes.splitlines()
    numbered_notes = "\\n".join(
        f"[{i}] {line}"
        for i, line in enumerate(lines, start=1)
    )

    # Validate all criteria before making model calls.
    for criterion in criteria:
        if not criterion.criterion_name or not criterion.requirement:
            raise ValueError(f"Criterion object is missing required fields: {criterion}")

    for criterion in criteria:
        resp = client.messages.parse(
            model="claude-sonnet-5",
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": f"""
You are a clinical evidence locator.

Your task is to find the clinical-note lines directly relevant to ONE
insurance coverage criterion.

Coverage criterion:
{criterion.requirement}

Numbered clinical notes:
{numbered_notes}

Instructions:
- Return only source line ranges directly relevant to the criterion.
- Evidence must address the same clinical subject, treatment, condition,
  or activity as the criterion.
- Generic similarities such as program, treatment, or participation
  are not sufficient to establish relevance.
- If the clinical note does not address the required subject,
  return an empty ranges list.
- Never select unrelated evidence just to provide an answer.
- Include evidence that supports or contradicts the criterion.
- Include relevant dates, measurements, medication history, and
  explicit negative statements.
- Select complete source lines.
- Use separate ranges for evidence in nonconsecutive locations.
- Exclude unrelated medical history and administrative details.
- Do not treat future plans as proof of completed activities.
- Do not calculate durations or determine whether the criterion is met.
- Do not invent evidence or line numbers.
- If no relevant evidence exists, return an empty ranges list.
- Return only the structured JSON requested by the schema.
"""
            }],
            output_format=EvidenceRanges,
        )

        if resp.parsed_output is None:
            raise RuntimeError(
                f"Stage 3 failed to produce structured output for "
                f"criterion: {criterion.criterion_name}"
            )

        extracted = []

        for selected in resp.parsed_output.ranges:
            line_start = selected.start
            line_end = selected.end

            if not (1 <= line_start <= line_end <= len(lines)):
                raise RuntimeError(
                    f"Stage 3 returned invalid line range "
                    f"{line_start}-{line_end} for "
                    f"criterion: {criterion.criterion_name}"
                )

            note_text = "\n".join(lines[line_start - 1:line_end])

            evidence = NoteEvidence(
                note_text=note_text,
                line_start=line_start,
                line_end=line_end,
            )

            if not verify_quote_lines(notes, evidence):
                raise RuntimeError(
                    f"Stage 3 evidence verification failed for "
                    f"criterion: {criterion.criterion_name}"
                )

            evidence_key = (
                line_start,
                line_end,
                note_text,
            )

            if evidence_key in evidence_ids:
                evidence.evidence_id = evidence_ids[evidence_key]
            else:
                evidence.evidence_id = f"E{evidence_counter}"
                evidence_ids[evidence_key] = evidence.evidence_id
                evidence_counter += 1

            extracted.append(evidence)

        result.append(
            CriterionEvidence(
                criterion_name=criterion.criterion_name,
                requirement=criterion.requirement,
                evidence=extracted,
            )
        )

    return result

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
    result = notes_extraction(notes_text, criteria)
    print(result)