import requests
from bs4 import BeautifulSoup


def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    try:
        return BeautifulSoup(raw_html, "html.parser").get_text().strip()
    except Exception as e:
        print(f"Failed to clean HTML: {e}")
        return raw_html

def fetch_article_content(url: str) -> str:
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
    except Exception as e:
        print(f"Failed to fetch article content from {url}: {e}")
        return ""
