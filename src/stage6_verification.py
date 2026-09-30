from pydantic import BaseModel
from stage1_extraction import extract_denial_info
from stage2_lookup import extract_criteria, policy_files
from stage3_evidence_extraction import NoteEvidence, notes_extraction, verify_quote_lines
from stage4_sufficiency_judgement import SufficiencyJudgment, sufficiency_judgment
from stage5_generation import AppealDraft, generate_appeal
import anthropic
from dotenv import load_dotenv
from pathlib import Path
import re

load_dotenv()
client = anthropic.Anthropic()

class VerificationFinding(BaseModel):
    check_name: str
    claim: str
    evidence_ids: list[str]
    reason: str

def classify_numeric_value(sentence: str, value: str):

    resp = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": f"""
                    Classify the role of the value "{value}" in the sentence below.

                    Return EXACTLY one of:
                    raw_clinical
                    computed
                    policy

                    raw_clinical = a patient-specific value directly documented as that exact value
                    in the clinical record, such as BMI, weight, age, date of birth, dose, or visit date.

                    computed = a patient-specific value that represents a calculation or derivation
                    from other clinical facts, even if the sentence states the result directly.
                    Examples include duration of participation calculated from start/end dates,
                    change in weight, percentage change, or other derived quantities.

                    policy = a value describing an insurance policy requirement or threshold.

                    Do not determine whether the value is correct.
                    Only classify its role.

                    Sentence:
                    {sentence}
                    """
            }
        ]
    )
    
    result = next(
        block.text.strip()
        for block in resp.content
        if block.type == "text"
    )

    if result not in {"raw_clinical", "computed", "policy"}:
        raise RuntimeError(
            f"Unexpected numeric classification: {result}"
        )

    return result

def check_citation_coverage(clinical_policy_support: str):
    findings = []

    for sentence in clinical_policy_support.split('. '):
        sentence = sentence.strip()
        if not sentence:
            continue
        if not re.search(r'\[E\d+\]', sentence):
            findings.append(
                VerificationFinding(
                    check_name="citation_coverage",
                    claim=sentence,
                    evidence_ids=[],
                    reason="Clinical policy support sentence is missing an evidence citation."
                )
            )
    
    return findings


def check_citation_existence(clinical_policy_support: str, evidence_ids: list[str]):
    findings = []

    for sentence in clinical_policy_support.split('. '):
        sentence = sentence.strip()

        cited_ids = re.findall(r'\[(E\d+)\]', sentence)

        for evidence_id in cited_ids:
            if evidence_id not in evidence_ids:
                findings.append(
                    VerificationFinding(
                        check_name="citation_existence",
                        claim=sentence,
                        evidence_ids=[evidence_id],
                        reason="Clinical policy support sentence contains an evidence citation that is not present in sufficiency judgment results."
                    )
                )
    return findings


def check_numbers_and_dates(clinical_policy_support: str, evidence_lookup: dict[str, str]):
    findings = []

    for sentence in clinical_policy_support.split(". "):
        sentence = sentence.strip()

        cited_ids = re.findall(r'\[(E\d+)\]', sentence)

        if not cited_ids:
            continue

        cited_evidence_text = " ".join(
            evidence_lookup[evidence_id]
            for evidence_id in cited_ids
            if evidence_id in evidence_lookup
        )

        values = re.findall(
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d+(?:\.\d+)?\b',
            sentence
        )

        for value in values:

            value_type = classify_numeric_value(sentence, value)

            # Milestone 4 only checks raw clinical values
            if value_type != "raw_clinical":
                continue

            if value not in cited_evidence_text:
                findings.append(
                    VerificationFinding(
                        check_name="numbers_and_dates",
                        claim=sentence,
                        evidence_ids=cited_ids,
                        reason=f"Clinical value '{value}' does not appear in the cited evidence."
                    )
                )

    return findings


def check_computed_value(value: str, computed_span_months: int, sentence: str, cited_ids: list[str]):
    findings = []

    if float(value) != float(computed_span_months):
        findings.append(
            VerificationFinding(
                check_name="computed_value",
                claim=sentence,
                evidence_ids=cited_ids,
                reason=(
                    f"Computed value '{value}' does not match "
                    f"Stage 4 computed span of '{computed_span_months}' months."
                )
            )
        )

    return findings


def check_stage4_consistency(clinical_policy_support: str, criterion_name: str, requirement: str, status: str, reasoning: str, missing: str):
    resp = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=300,
    messages=[
        {
        "role": "user",
        "content": f"""
        You are verifying whether an appeal accurately represents
        a prior sufficiency judgment.

        STAGE 4 SUFFICIENCY JUDGMENT

        Criterion:
        {criterion_name}

        Requirement:
        {requirement}

        Status:
        {status}

        Reasoning:
        {reasoning}

        Missing:
        {missing}

        STAGE 5 CLINICAL POLICY SUPPORT

        {clinical_policy_support}

        Determine whether Stage 5 contradicts or overstates the
        Stage 4 sufficiency judgment for this criterion.

        Return EXACTLY one of:
        consistent
        contradiction

        A contradiction means Stage 5 claims the criterion is satisfied,
        or makes a stronger claim than Stage 4 supports.

        Do not independently judge the clinical evidence.
        Do not determine whether Stage 4 was correct.
        Only compare Stage 5 against the Stage 4 judgment.
        """
        }
        ]
    )

    result = next(block.text.strip() for block in resp.content if block.type == "text")

    if result not in {"consistent", "contradiction"}:
        raise RuntimeError(f"Unexpected Stage 4 consistency result: {result}")

    if result == "consistent":
        return []

    return [
        VerificationFinding(
            check_name="stage4_consistency",
            claim=clinical_policy_support,
            evidence_ids=re.findall(
                r'\[(E\d+)\]',
                clinical_policy_support
                ),
            reason=(
                f"Stage 5 contradicts or overstates the Stage 4 "
                f"judgment for criterion '{criterion_name}'."
                )
        )
    ]


def check_semantic_support(
    claim: str,
    cited_evidence: dict[str, str]
):
    resp = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""
                You are verifying whether the cited clinical evidence
                supports a claim made in a prior authorization appeal.

                CLAIM:
                {claim}

                CITED EVIDENCE:
                {cited_evidence}

                Determine whether the cited evidence supports the claim.

                Return EXACTLY one of:
                supported
                unsupported

                supported = the cited evidence provides sufficient support
                for the clinical claim.

                unsupported = the cited evidence does not support the claim,
                or the claim says more than the cited evidence establishes.

                Only use the cited evidence provided above.
                Do not assume facts that are not present.
                Do not use outside medical knowledge.
                Do not determine whether the insurance policy is satisfied.
                Only determine whether the cited evidence supports the claim.
                """
            }
        ]
    )

    result = next(
        block.text.strip()
        for block in resp.content
        if block.type == "text"
    )

    if result not in {"supported", "unsupported"}:
        raise RuntimeError(
            f"Unexpected semantic support result: {result}"
        )

    if result == "supported":
        return []

    return [
        VerificationFinding(
            check_name="semantic_support",
            claim=claim,
            evidence_ids=list(cited_evidence.keys()),
            reason="The cited evidence does not support the clinical claim."
        )
    ]


def check_provenance(
    notes_text: str,
    evidence: list[NoteEvidence]
):
    findings = []

    for item in evidence:

        if not verify_quote_lines(notes_text, item):
            findings.append(
                VerificationFinding(
                    check_name="provenance",
                    claim=item.note_text,
                    evidence_ids=[item.evidence_id] if item.evidence_id else [],
                    reason=(
                        "Stored evidence does not match the claimed "
                        "source lines in the clinical notes."
                    )
                )
            )

    return findings


def verification(
    notes_text: str,
    stage4_results: list[SufficiencyJudgment],
    appeal_draft: AppealDraft
) -> list[VerificationFinding]:

    findings = []

    clinical_policy_support = appeal_draft.clinical_policy_support

    evidence_lookup = {}
    all_evidence = []

    # Build evidence data from Stage 4
    for judgment in stage4_results:
        for evidence in judgment.evidence:

            if evidence.evidence_id:
                evidence_lookup[evidence.evidence_id] = evidence.note_text

            if evidence not in all_evidence:
                all_evidence.append(evidence)

    evidence_ids = list(evidence_lookup.keys())


    # Citation coverage
    findings.extend(
        check_citation_coverage(clinical_policy_support)
    )


    # Citation existence
    findings.extend(
        check_citation_existence(
            clinical_policy_support,
            evidence_ids
        )
    )


    # Numbers and dates
    findings.extend(
        check_numbers_and_dates(
            clinical_policy_support,
            evidence_lookup
        )
    )


    # Stage 4 consistency
    for judgment in stage4_results:

        findings.extend(
            check_stage4_consistency(
                clinical_policy_support,
                judgment.criterion_name,
                judgment.requirement,
                judgment.status,
                judgment.reasoning,
                judgment.missing
            )
        )


    # Semantic support
    for sentence in clinical_policy_support.split(". "):

        sentence = sentence.strip()

        cited_ids = re.findall(
            r'\[(E\d+)\]',
            sentence
        )

        cited_evidence = {
            evidence_id: evidence_lookup[evidence_id]
            for evidence_id in cited_ids
            if evidence_id in evidence_lookup
        }

        if cited_evidence:
            findings.extend(
                check_semantic_support(
                    sentence,
                    cited_evidence
                )
            )


    # Provenance
    findings.extend(
        check_provenance(
            notes_text,
            all_evidence
        )
    )


    return findings


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent

    # Load denial letter
    file_path = (BASE_DIR/ "data"/ "cases"/ "cases_v1"/ "denial_letters"/ "case_001_denial.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        text_data = f.read()

    # Stage 1
    denial_info = extract_denial_info(text_data)

    # Stage 2
    payer = denial_info.payer.lower()
    policy_file_path = policy_files.get(payer)

    if policy_file_path:
        with open(policy_file_path, "r", encoding="utf-8") as f:
            policy_text = f.read()
    else:
        raise ValueError(
            f"No policy file found for payer: {denial_info.payer}"
        )

    criteria = extract_criteria(policy_text, denial_info)

    # Load clinical notes
    notes_file_path = (BASE_DIR/ "data"/ "cases"/ "cases_v1"/ "notes"/ "case_001_note.txt")

    with open(notes_file_path, "r", encoding="utf-8") as f:
        notes_text = f.read()

    # Stage 3
    evidence_results = notes_extraction(notes_text, criteria)

    # Stage 4
    sufficiency_results = sufficiency_judgment(evidence_results)

    # Stage 5
    draft = generate_appeal(
        denial_info,
        sufficiency_results
    )

    # Stage 6
    findings = verification(
        notes_text,
        sufficiency_results,
        draft
    )

    print(findings)