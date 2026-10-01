from stage1_extraction import extract_denial_info, DenialInfo
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
client = genai.Client()

BASE_DIR = Path(__file__).resolve().parent.parent

class Criterion(BaseModel):
    criterion_name: str
    requirement: str
    policy_reference: str | None = None

def extract_criteria(policy_text: str, denial_info: DenialInfo) -> list[Criterion]:
    resp = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"""Policy text: {policy_text} Denial information: {denial_info} Extract all coverage criteria from the supplied policy that apply to this specific prior authorization request. Return each applicable criterion as a separate Criterion object. For criterion_name: - Return a short descriptive name for the criterion. For requirement: - Return the specific policy requirement or condition that must be satisfied. For policy_reference: - Return the relevant policy section or reference if available. - Otherwise return None. Only include criteria explicitly supported by the supplied policy text. Use the denial information only to identify the relevant drug, indication, request type, and policy pathway. Do not infer, invent, or add requirements that are not present in the policy. Do not determine whether the patient satisfies the criteria. """,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[Criterion],
            max_output_tokens=3000,
        ),
    )

    return resp.parsed

policy_files = {
    "cigna": BASE_DIR / "data" / "policies" / "policies_txt" / "cigna_glp1_prior_auth.txt",
    "aetna": BASE_DIR / "data" / "policies" / "policies_txt" / "aetna_glp1_weight_management.txt",
    "unitedhealthcare": BASE_DIR / "data" / "policies" / "policies_txt" / "uhc_weight_loss_prior_auth.txt",
}

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
        policy_text = ""
    result = extract_criteria(policy_text, denial_info)
    print(result)