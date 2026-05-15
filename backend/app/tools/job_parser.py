import requests
from bs4 import BeautifulSoup

def scrape_job(url: str) -> str:
    headers ={
        "User-Agent": "Mozilla/5.0"
    }

    response =requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    text = soup.get_text(separator="\n")

    return text
