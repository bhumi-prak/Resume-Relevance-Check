# backend/parsing.py
import os
import re
import pdfplumber
import docx2txt
from backend.logger import get_logger

logger = get_logger("parsing")

def extract_text_from_pdf(path: str) -> str:
    text_chunks = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                txt = page.extract_text()
                if txt:
                    text_chunks.append(txt)
    except Exception as e:
        print(f"[extract_text_from_pdf] error for {path}: {e}")
    return "\n".join(text_chunks)

def extract_text_from_docx(path: str) -> str:
    try:
        text = docx2txt.process(path)
        return text or ""
    except Exception as e:
        print(f"[extract_text_from_docx] error for {path}: {e}")
        return ""

def extract_text_from_txt(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"[extract_text_from_txt] error for {path}: {e}")
        return ""

def clean_text(text: str) -> str:
    if not text:
        return ""
    # Normalize whitespace
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{2,}', '\n\n', text)
    # Remove weird non-printable chars
    text = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\u00A0-\uFFFF]', ' ', text)
    text = text.strip()
    return text

def extract_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        raw = extract_text_from_pdf(path)
    elif ext in [".docx", ".doc"]:
        raw = extract_text_from_docx(path)
    elif ext in [".txt", ".md"]:
        raw = extract_text_from_txt(path)
    else:
        # attempt docx extraction as fallback
        raw = extract_text_from_docx(path)
    return clean_text(raw)

