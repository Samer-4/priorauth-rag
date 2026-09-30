from stage1_extraction import extract_denial_info, DenialInfo  
from stage2_lookup import extract_criteria, policy_files
from stage3_evidence_extraction import notes_extraction
from stage4_sufficiency_judgement import sufficiency_judgment, SufficiencyJudgment
import anthropic
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path  
from datetime import date

load_dotenv()
client = anthropic.Anthropic()

BASE_DIR = Path(__file__).resolve().parent.parent

class AppealDraft(BaseModel):
    appeal_request: str
    denial_basis: str
    clinical_policy_support: str
    reconsideration_request: str

def generate_appeal(denial_info: DenialInfo, sufficiency_results: list[SufficiencyJudgment]) -> AppealDraft:
    resp = client.messages.parse(
        model = "claude-sonnet-5",
        max_tokens = 4000,
        messages = [{
            "role": "user",
            "content": f"""
            You are generating the content for a prior-authorization appeal draft.

            Use ONLY the denial information and sufficiency judgment results provided below.

            Denial information:
            {denial_info}

            Sufficiency judgment results:
            {sufficiency_results}

            Fill the four fields of the AppealDraft output as follows:

            1. appeal_request:
            Briefly state what prior-authorization denial is being appealed, identify the medication when available, and request reconsideration.

            2. denial_basis:
            Accurately describe the payer's stated reason for denial and the relevant coverage requirement. Do not invent additional denial reasons or policy requirements.

            3. clinical_policy_support:
            Present the clinical and policy-based support for the appeal using only the supplied requirements, evidence, and sufficiency judgments.
            - If a criterion is "satisfied", you may state that the evidence supports meeting the requirement.
            - If a criterion is "partial", describe only the supported portions and do not claim the full requirement is met.
            - If a criterion is "not_satisfied", do not claim that the requirement has been met.
            - Preserve any uncertainty or missing documentation identified in the sufficiency judgments.
            - Preserve uncertainty exactly when the sufficiency judgment identifies ambiguous dates, timing, duration, or missing documentation.
            - Do not convert an uncertain or inferred timeline into a definitive chronological claim.
            - Do not state that an event occurred "prior to," "after," or "before" another event unless that ordering is explicitly supported by the supplied information.
            - Do not infer causation from clinical facts. For example, do not state that a weight change, plateau, or other clinical event caused a treatment decision unless the supplied evidence explicitly states that relationship.
            - Only discuss a coverage criterion as being met if that criterion is included in the supplied sufficiency judgments and its status is "satisfied".
            - Focus the appeal on the criterion or criteria relevant to the stated denial basis.
            - Do not introduce unrelated unmet, unsupported, or administrative policy criteria unless they are necessary to accurately address the denial.

            4. reconsideration_request:
            - Briefly summarize the supported basis for reconsideration and request approval when supported by the supplied information. Do not introduce new evidence.
            - Do not volunteer missing information about unrelated policy criteria that are not part of the stated denial basis.

            Grounding rules:
            - Use ONLY information explicitly contained in the supplied denial information and sufficiency judgments.
            - Do not invent, assume, or infer unsupported patient facts.
            - Do not fabricate diagnoses, treatments, dates, measurements, medication history, outcomes, or clinical events.
            - Do not introduce outside medical knowledge, clinical guidelines, or policy requirements.
            - Do not change, override, or contradict the supplied sufficiency judgments.
            - Do not claim a criterion is satisfied unless its status is "satisfied".
            - Do not overstate evidence to make the appeal more persuasive.
            - Do not mention Claude, the pipeline, Stage 1, Stage 2, Stage 3, Stage 4, or other internal implementation details.
            - Do not use "satisfied", "partial", or "not_satisfied" as internal system labels in the appeal prose.
            - Keep the writing professional, concise, factual, and appropriate for insurer review.
            - The output is a DRAFT for human review and must remain fully grounded in the supplied information.

            Evidence citation rules:
            - Every clinical factual claim in clinical_policy_support must be followed by one or more evidence IDs that directly support that claim.
            - Use the evidence_id values exactly as provided in the sufficiency judgment results, formatted in square brackets, for example [E2] or [E2] [E4].
            - Cite only evidence that directly supports the claim immediately before the citation.
            - Do not invent evidence IDs.
            - Do not cite an evidence ID that is not present in the supplied sufficiency judgment results.
            - If a clinical claim cannot be directly supported by the supplied evidence, do not include that claim.
            - Place all supporting evidence citation tags at the end of the clinical sentence they support.
            """
        }],
        output_format = AppealDraft,
    )

    if resp.parsed_output is None:
        raise RuntimeError(
            "Stage 5 failed to produce a structured appeal draft"
        )
    
    return resp.parsed_output

def render_appeal(draft: AppealDraft, case_info: DenialInfo) -> str:

    current_date = date.today().strftime("%m/%d/%Y")

    return f"""
    {current_date}

    RE: PRIOR AUTHORIZATION APPEAL

    Patient: {case_info.member.patient_name}
    DOB: {case_info.member.dob}
    Member ID: {case_info.member.member_id}
    Medication: {case_info.drug}
    Policy: {case_info.cited_policy_reference}

    To Whom It May Concern:

    {draft.appeal_request}

    DENIAL BASIS

    {draft.denial_basis}

    CLINICAL AND POLICY SUPPORT

    {draft.clinical_policy_support}

    RECONSIDERATION REQUEST

    {draft.reconsideration_request}

    Sincerely,

    {case_info.prescriber.name}
    {case_info.prescriber.credentials}

    DRAFT — FOR HUMAN REVIEW
    """

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
    draft = generate_appeal(denial_info, sufficiency_results)
    appeal_letter = render_appeal(draft, case_info=denial_info)
    print(appeal_letter)