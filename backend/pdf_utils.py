import io
from PyPDF2 import PdfReader

def extract_pdf_text(file_bytes):
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        return text.strip()

    except Exception as e:
        print("PDF ERROR:", e)
        return ""