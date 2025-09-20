from backend.parsing import extract_text

def test_pdf_parsing():
    text = extract_text("data/resumes/resume1.pdf")
    assert len(text) > 0, "PDF parsing failed"

def test_docx_parsing():
    text = extract_text("data/resumes/resume2.docx")
    assert len(text) > 0, "DOCX parsing failed"
