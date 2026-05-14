from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def crawl_website(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox"]
            )

            page = browser.new_page()

            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            html = page.content()

            browser.close()

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned_text = "\n".join(lines)

        cleaned_text = cleaned_text[:15000]

        return [cleaned_text] if cleaned_text else []

    except Exception as e:
        print("❌ CRAWLER ERROR:", str(e))
        return []