from stage1_extraction import extract_denial_info
from stage2_lookup import extract_criteria, Criterion, policy_files
import anthropic
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
client = anthropic.Anthropic()

BASE_DIR = Path(__file__).resolve().parent.parent

class NoteEvidence(BaseModel):
    note_text: str

class CriterionEvidence(BaseModel):
    criterion_name: str
    requirement: str
    evidence: list[NoteEvidence]

def notes_extraction(notes: str, criteria: list[Criterion]) -> list[CriterionEvidence]:
    result = []
    for criterion in criteria:
        if not criterion.criterion_name or not criterion.requirement:
            raise ValueError(f"Criterion object is missing required fields: {criterion}")
        
        resp = client.messages.parse(
            model = "claude-sonnet-5",
            max_tokens = 4000,
            messages = [{
                "role": "user",
                "content": f"""
                Clinical notes:
                {notes}

                Coverage criterion:
                {criterion}

                Extract all text from the clinical notes that is directly relevant to the supplied coverage criterion.

                Rules:
                - Return each distinct piece of relevant evidence as a separate NoteEvidence object.
                - For note_text, copy the relevant text exactly as it appears in the clinical notes.
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
                """
                }],
            output_format = list[NoteEvidence],
        )
        result.append(CriterionEvidence(
            criterion_name=criterion.criterion_name,
            requirement=criterion.requirement,
            evidence=resp.parsed_output
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