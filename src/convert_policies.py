import pymupdf
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
filepath = BASE_DIR / "data" / "policies" / "policies_pdf"

for pdf_path in filepath.glob("*.pdf"):
    with pymupdf.open(pdf_path) as pdf:
        txt_path = (BASE_DIR / "data" / "policies" / "policies_txt" / f"{pdf_path.stem}.txt")
        text = ""
        for page in pdf:
            text += page.get_text()
    txt_path.write_text(text, encoding="utf-8")
    