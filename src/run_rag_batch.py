import argparse
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT))

from stage1_extraction import extract_denial_info
from stage2_rag_adapter import extract_criteria_with_rag


def get_route(denial, text):
    """Use explicit case information; never invent a policy pathway."""
    payer = denial.payer.strip().lower()
    drug = denial.drug.strip()
    body = text.lower()

    if payer not in {"aetna", "cigna", "unitedhealthcare"}:
        raise ValueError(f"Unsupported payer: {payer}")

    if re.search(r"\b(reauthorization|renewal|continuation of therapy)\b", body):
        pathway = "continuation"
    elif re.search(r"\b(initial authorization|initial therapy|new start|first-time request)\b", body):
        pathway = "initial"
    else:
        raise ValueError("Authorization pathway not established by the letter")

    scope = None

    if payer == "unitedhealthcare":
        if "north dakota" in body or "fully insured ehb" in body:
            scope = "north_dakota"
        else:
            raise ValueError("UHC coverage scope not established")

        if "wegovy" not in drug.lower():
            raise ValueError("UHC medication not yet supported")

        medication = (
            "Wegovy tablet" if "tablet" in drug.lower()
            else "Wegovy injection" if "injection" in drug.lower()
            else "Wegovy"
        )
        indication = "weight loss"

    elif payer == "aetna":
        if "wegovy" not in drug.lower():
            raise ValueError("Aetna medication not yet validated")

        medication = "Wegovy"
        indication = "Chronic Weight Management (Adult)"

    else:
        lower_drug = drug.lower()

        if "wegovy" in lower_drug:
            if "tablet" in lower_drug:
                medication = "Wegovy tablet"
            elif "injection" in lower_drug:
                medication = "Wegovy injection"
            else:
                raise ValueError("Wegovy formulation not established")
        else:
            raise ValueError("Cigna medication not yet validated")

        indication = "Weight Loss in an Adult"

    if not any(
        term in body
        for term in ("weight loss", "weight management", "obesity", "overweight", "bmi")
    ):
        raise ValueError("Weight-management indication not established")

    member = getattr(denial, "member", None)
    age = getattr(member, "age", None)

    if payer in {"aetna", "cigna"} and (age is None or age < 18):
        raise ValueError("Adult eligibility pathway not established")

    return {
        "medication": medication,
        "indication": indication,
        "pathway": pathway,
        "scope": scope,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cases",
        default="data/cases/cases_v1/denial_letters",
    )
    parser.add_argument(
        "--output",
        default="evaluation/results/rag_stage2_batch.json",
    )
    args = parser.parse_args()

    files = sorted(Path(args.cases).glob("*.txt"))
    if not files:
        raise SystemExit(f"No denial letters found in {args.cases}")

    print(f"Found {len(files)} denial letters")

    results = []

    for number, path in enumerate(files, 1):
        print(f"\n[{number}/{len(files)}] {path.name}", flush=True)

        record = {
            "case": path.name,
            "status": "pending",
        }

        try:
            text = path.read_text(encoding="utf-8")

            denial = extract_denial_info(text)
            route = get_route(denial, text)

            criteria = extract_criteria_with_rag(
                denial,
                medication=route["medication"],
                indication=route["indication"],
                pathway=route["pathway"],
                scope=route["scope"],
            )

            if not criteria:
                raise ValueError("Stage 2 returned no criteria")

            record.update({
                "status": "completed",
                "payer": denial.payer,
                "route": route,
                "criteria": [c.model_dump() for c in criteria],
            })

            print(f"Completed: {len(criteria)} criteria", flush=True)

        except Exception as exc:
            record.update({
                "status": "needs_review",
                "error": f"{type(exc).__name__}: {exc}",
            })
            print(f"Needs review: {exc}", flush=True)

        results.append(record)

        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(results, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    completed = sum(r["status"] == "completed" for r in results)

    print(f"\nFINISHED: {completed}/{len(results)} completed")
    print(f"Needs review: {len(results) - completed}")
    print(f"Report: {args.output}")


if __name__ == "__main__":
    main()
