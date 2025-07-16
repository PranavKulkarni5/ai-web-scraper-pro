# scrape.py
import requests
from bs4 import BeautifulSoup

def scrape_website(website: str) -> str:
    """
    Fetches raw HTML of the page via a simple HTTP GET.
    """
    resp = requests.get(website, timeout=10)
    resp.raise_for_status()
    return resp.text

def extract_body_content(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.body
    return str(body) if body else ""

def clean_body_content(body_content: str) -> str:
    soup = BeautifulSoup(body_content, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # strip blank lines
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())

def split_dom_content(dom_content: str, max_length: int = 6000) -> list[str]:
    return [dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)]
