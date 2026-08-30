from stage1_extraction import extract_denial_info, DenialInfo
import anthropic
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
client = anthropic.Anthropic()

BASE_DIR = Path(__file__).resolve().parent.parent

class Criterion(BaseModel):
    criterion_name: str
    requirement: str
    policy_reference: str | None = None

def extract_criteria(policy_text: str, denial_info: DenialInfo) -> Criterion:
    resp = client.messages.parse(
        model = "claude-sonnet-5",
        max_tokens = 3000,
        messages = [{"role": "user", "content": f"Take the input text: {policy_text}, {denial_info} and extract the necessary fields required as per Criterion model. For criterion_name: return a short category or name. For requirement: return the specific requirement or condition that is relevant to the denial. For policy_reference: return any cited policy reference if available, otherwise return None. Only return requirements explicitly supported by the supplied policy text. Do not infer or invent missing requirements."}],
        output_format = Criterion,
    )
    return resp.parsed_output

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