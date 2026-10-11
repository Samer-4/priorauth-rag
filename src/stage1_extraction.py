from llm_client import get_client
from pydantic import BaseModel, Field
from pathlib import Path
from dotenv import load_dotenv
from typing import Literal

load_dotenv()
client = get_client()

class MemberClinicalProfile(BaseModel):
    patient_name: str | None = None
    member_id: str | None = None
    dob: str | None = None
    age: int | None = None
    bmi: float | None = None

class PrescriberInfo(BaseModel):
    name: str | None = None
    credentials: str | None = None
    
class DenialInfo(BaseModel):
  payer: Literal["cigna", "aetna", "unitedhealthcare"]
  drug: str
  denial_reason : str = Field(
        description="The primary denial determination as a concise 2-5 word category-style phrase. "
        "If the letter contains an explicit determination, denial heading, decision label, "
        "or stated primary denial reason, use that value instead of a more detailed supporting rationale. "
        "Only infer the denial reason from clinical rationale or bullet-point details when no explicit "
        "determination is provided.")
  cited_policy_reference: str | None = None
  cited_requirement_text: str | None = None
  # Policy-routing information for Stage 2 RAG.
  # Extract from the denial letter; never guess missing details.
  policy_medication: str | None = Field(
      default=None,
      description="Medication name and formulation as referenced by the cited policy, "
      "for example Wegovy injection, Wegovy tablet, or liraglutide. "
      "Do not invent a formulation."
  )
  indication: str | None = Field(
      default=None,
      description="Specific coverage indication or policy subsection cited in the "
      "denial, including adult versus pediatric and any disease-specific indication. "
      "Preserve the policy wording when available."
  )
  pathway: Literal["initial", "continuation"] | None = Field(
      default=None,
      description="Initial authorization versus continuation or reauthorization, "
      "based on the denial letter."
  )
  scope: Literal["general", "north_dakota"] | None = Field(
      default=None,
      description="For UnitedHealthcare only: north_dakota when the letter explicitly "
      "identifies a North Dakota fully insured EHB plan; general when the letter "
      "explicitly identifies the standard plan pathway. Otherwise null."
  )
  member: MemberClinicalProfile
  prescriber: PrescriberInfo

def extract_denial_info(text_data: str) -> DenialInfo:
    resp = client.messages.parse(
        model = "claude-sonnet-5",
        max_tokens = 3000,
        messages = [{"role": "user", "content": f"Take the input text: {text_data} and extract the necessary fields required as per DenialInfo model. For denial_reason: Return a concise 2-5 word category-style phrase. Prioritize an explicitly stated denial determination, decision, heading, or primary denial reason. Do not replace an explicit determination with a more specific supporting clinical rationale. Only infer the denial reason from detailed rationale if no explicit determination is present. Only extract member and prescriber information explicitly stated in the input text. For Stage 2 policy retrieval, also extract: policy_medication, indication, pathway, and scope. Use the explicit requested drug, formulation, review type, plan information, and cited policy subsection. Keep the original drug field unchanged. For policy_medication, prefer the medication naming used by the cited policy when supported by the letter. For indication, preserve the specific cited policy category, including adult versus pediatric, weight management versus cardiovascular risk, or obstructive sleep apnea when applicable. Set pathway to initial for an initial authorization request and continuation for a continuation or reauthorization request. For UHC, use north_dakota only when the plan explicitly identifies North Dakota fully insured EHB coverage; use general only when the standard plan scope is established. For other insurers, scope must be null. Never infer a missing coverage detail from the case number. If a field is not present, return null."}],
        output_format = DenialInfo,
    )
    return resp.parsed_output

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data" / "cases" / "cases_v1" / "denial_letters" / "case_001_denial.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        text_data = f.read()
    result = extract_denial_info(text_data)
    print(result)