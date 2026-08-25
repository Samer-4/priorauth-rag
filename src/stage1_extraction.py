import anthropic
from pydantic import BaseModel, Field
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

class MemberClinicalProfile(BaseModel):
    age: int | None
    bmi: float | None

class DenialInfo(BaseModel):
  payer: str
  drug: str
  denial_reason : str = Field(
        description="The primary denial determination as a concise 2-5 word category-style phrase. "
        "If the letter contains an explicit determination, denial heading, decision label, "
        "or stated primary denial reason, use that value instead of a more detailed supporting rationale. "
        "Only infer the denial reason from clinical rationale or bullet-point details when no explicit "
        "determination is provided.")
  cited_policy_reference: str | None
  cited_requirement_text: str | None
  member: MemberClinicalProfile

def extract_denial_info(text_data: str) -> DenialInfo:
    resp = client.messages.parse(
        model = "claude-sonnet-5",
        max_tokens = 3000,
        messages = [{"role": "user", "content": f"Take the input text: {text_data} and extract the necessary fields required as per DenialInfo model. For denial_reason: Return a concise 2-5 word category-style phrase. Prioritize an explicitly stated denial determination, decision, heading, or primary denial reason. Do not replace an explicit determination with a more specific supporting clinical rationale. Only infer the denial reason from detailed rationale if no explicit determination is present."}],
        output_format = DenialInfo,
    )
    return resp.parsed_output

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data" / "cases" / "denial_letters" / "case_001_denial.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        text_data = f.read()
    result = extract_denial_info(text_data)
    print(result)