from stage1_extraction import extract_denial_info
from stage2_lookup import extract_criteria, Criterion, policy_files
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import re

load_dotenv()
client = genai.Client()

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

    for criterion in criteria:
        if not criterion.criterion_name or not criterion.requirement:
            raise ValueError(f"Criterion object is missing required fields: {criterion}")
        
        resp = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"""
            Clinical notes:
            {notes}

            Coverage criterion:
            {criterion}

            Extract all text from the clinical notes that is directly relevant to the supplied coverage criterion.

            Rules:
            - Group consecutive relevant lines into a single NoteEvidence object when they form one coherent piece of evidence about the same topic or clinical fact.
            - If the meaning or topic changes, return the text as a separate NoteEvidence object, even if the lines are consecutive.
            - If relevant evidence appears in separate locations in the clinical notes, return each location as a separate NoteEvidence object.
            - Do not split a continuous passage into separate NoteEvidence objects merely because it spans multiple lines.
            - For note_text, copy the relevant text exactly as it appears in the clinical notes.
            - Preserve the original spacing, punctuation, and line breaks exactly as they appear in the clinical notes.
            - Do not join separate lines together or split a line into multiple lines.
            - Evidence must preserve complete source lines.
            - If any portion of a source line is relevant, include that entire source line in note_text.
            - Never return only part of a source line.
            - Do not reformat or normalize whitespace in note_text.
            - Do not paraphrase, summarize, rewrite, or modify the text.
            - Only return evidence explicitly present in the clinical notes.
            - Do not infer or assume any clinical fact that is not explicitly stated.
            - Do not calculate or derive new information from dates, measurements, or other values.
            - Do not determine whether the evidence satisfies, fails, supports, or refutes the coverage criterion.
            - Include explicit negative statements when they are relevant, such as documentation that a treatment, medication, diagnosis, or event did not occur.
            - Do not infer absence from missing information. Something is absent only when the clinical notes explicitly state that it is absent.
            - The coverage criterion is provided only to determine which parts of the clinical notes are relevant.
            - If no relevant evidence is explicitly present in the clinical notes, return an empty list [].
            - Never invent evidence in order to avoid returning an empty list.
            """,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=list[NoteEvidence],
                max_output_tokens=8000,
            ),
        )

        if resp.parsed is None:
            raise RuntimeError(
                f"Stage 3 failed to produce structured output for "
                f"criterion: {criterion.criterion_name}"
            )

        for evidence in resp.parsed:
            line_start, line_end = find_quote_lines(notes, evidence.note_text)

            evidence.line_start = line_start
            evidence.line_end = line_end

            if not verify_quote_lines(notes, evidence):
                raise RuntimeError(
                    f"Stage 3 evidence verification failed for "
                    f"criterion: {criterion.criterion_name}"
                )

            evidence_key = (
                line_start,
                line_end,
                evidence.note_text
            )

            if evidence_key in evidence_ids:
                evidence.evidence_id = evidence_ids[evidence_key]

            else:
                evidence.evidence_id = f"E{evidence_counter}"
                evidence_ids[evidence_key] = evidence.evidence_id
                evidence_counter += 1

        result.append(CriterionEvidence(
            criterion_name=criterion.criterion_name,
            requirement=criterion.requirement,
            evidence=resp.parsed
        ))

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