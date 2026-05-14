import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


def crawl_website(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header"
        ]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        cleaned_text = "\n".join(lines)

        cleaned_text = cleaned_text[:15000]

        return [cleaned_text]

    except Exception as e:

        print("CRAWLER ERROR:", str(e))

        return []


def extract_pdf_text(file):

    try:

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return [text.strip()]

    except Exception as e:

        print("PDF ERROR:", str(e))

        return []