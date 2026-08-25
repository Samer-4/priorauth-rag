import json
from stage1_extraction import extract_denial_info, DenialInfo
from pathlib import Path
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def validate_json(result: DenialInfo, labels: dict) -> bool:
    """
    Validate the extracted result against the provided labels.
    """
    status = True
    result_dict = result.model_dump()
    for key, value in result_dict.items():
        if key in labels:
            if key == "drug":
                if not drug_matches(value, labels[key]):
                    status = False
            elif key == "payer":
                if not payer_matches(value, labels[key]):
                    status = False
            elif key == "denial_reason":
                if not denial_reason_matches(value, labels[key]):
                    status = False
            elif value.lower() != labels[key].lower():
                status = False
    return status

def drug_matches(result_drug: str, label_drug: str) -> bool:
    result_lower = result_drug.lower()
    label_terms = label_drug.lower().replace("(", "").replace(")", "").split()
    return all(term in result_lower for term in label_terms)

def payer_matches(result_payer: str, label_payer: str) -> bool:
    result_lower = result_payer.lower().strip()
    label_terms = label_payer.lower().strip()
    return label_terms in result_lower or result_lower in label_terms


def denial_reason_matches(result_reason: str, label_reason: str) -> bool:
    result = result_reason.lower().replace("-", " ").replace("_", " ").strip()
    label = label_reason.lower().replace("-", " ").replace("_", " ").strip()

    if label in result or result in label:
        return True

    result_embedding = model.encode(result)
    label_embedding = model.encode(label)
    score = model.similarity(result_embedding, label_embedding)
    
    return float(score) >= 0.65


def score():
    score = 0
    count = 0

    for file in file_path.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text_data = f.read()
            count += 1
        label_file = labels_path / f"{file.stem}.json"
        if label_file.exists():
            with open(label_file, "r", encoding="utf-8") as f:
                labels = json.load(f)
            result = extract_denial_info(text_data)
            if validate_json(result, labels):
                score += 1

    text = f"Total files processed: {count}, Correctly extracted: {score}, Accuracy: {score/count if count > 0 else 0:.2f}"
    return text

if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data" / "cases" / "denial_letters"
    labels_path = BASE_DIR / "data" / "cases" / "denial_json"

    result_text = score()
    print(result_text)