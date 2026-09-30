from pydantic import BaseModel
from stage1_extraction import extract_denial_info
from stage2_lookup import extract_criteria, policy_files
from stage3_evidence_extraction import NoteEvidence, notes_extraction, verify_quote_lines
from stage4_sufficiency_judgement import SufficiencyJudgment, sufficiency_judgment
from stage5_generation import AppealDraft, generate_appeal
from stage6_verification import VerificationFinding, verification
from pathlib import Path


class CaseResult(BaseModel):
    case_id: str
    completed: bool
    error: str | None = None
    findings: list[VerificationFinding]
    
def run_case(case_id: str) -> CaseResult:
    base_dir = Path(__file__).resolve().parent.parent
    case_dir = base_dir / "data" / "cases" / "cases_v1"
    
    # Load denial letter
    denial_file_path = case_dir / "denial_letters" / f"{case_id}_denial.txt"
    with open(denial_file_path, "r", encoding="utf-8") as f:
        denial_text = f.read()
    denial_info = extract_denial_info(denial_text)
    
    # Load policy text
    payer = denial_info.payer.lower()
    policy_file_path = policy_files.get(payer)
    if policy_file_path:
        with open(policy_file_path, "r", encoding="utf-8") as f:
            policy_text = f.read()
    else:
        raise ValueError(
            f"No policy file found for payer: {denial_info.payer}"
        )
    
    # Extract criteria
    criteria = extract_criteria(policy_text, denial_info)
    
    # Load clinical notes
    notes_file_path = case_dir / "notes" / f"{case_id}_note.txt"
    with open(notes_file_path, "r", encoding="utf-8") as f:
        notes_text = f.read()
    
    # Extract evidence from notes
    try:
        evidence_results = notes_extraction(notes_text, criteria)
    except RuntimeError as error:
        return CaseResult(
            case_id=case_id,
            completed=False,
            error=str(error),
            findings=[]
        )
    
    # Perform sufficiency judgment
    sufficiency_results = sufficiency_judgment(evidence_results)
    
    # Generate appeal draft
    appeal_draft = generate_appeal(denial_info, sufficiency_results)
    
    # Verify appeal draft
    findings = verification(notes_text, sufficiency_results, appeal_draft)
    
    return CaseResult(case_id=case_id, completed=True, findings=findings)


if __name__ == "__main__":

    results = []

    for case_number in range(1, 31):
        case_id = f"case_{case_number:03d}"

        try:
            result = run_case(case_id)

        except Exception as error:
            result = CaseResult(
                case_id=case_id,
                completed=False,
                error=f"{type(error).__name__}: {error}",
                findings=[]
            )

        results.append(result)
        print(result)