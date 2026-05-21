import requests
from bs4 import BeautifulSoup


def get_dummy_job_description() -> str:
    return """
Data Scientist (m/f/d) - Customer Analytics

About the role:
We are looking for a Data Scientist to build and improve machine learning
solutions for customer and operations use cases. You will work closely with
product, engineering, and business stakeholders to turn data into measurable impact.

Key responsibilities:
- Build end-to-end ML workflows from data collection to model evaluation and deployment.
- Analyze large datasets to identify trends and actionable insights.
- Collaborate with cross-functional teams to define data-driven product improvements.
- Communicate findings clearly to technical and non-technical audiences.
- Improve data quality and support scalable analytics practices.

Required skills:
- Strong Python and SQL skills.
- Experience with machine learning workflows and model evaluation.
- Experience with ETL/data processing and dashboarding/reporting.
- Ability to communicate insights and collaborate across teams.

Nice to have:
- Cloud ML experience (AWS preferred).
- Experience with LLM/prompting applications.
- Exposure to Agile product development.
"""


def scrape_job(url: str) -> str:
    if not url or url.strip().lower() in {"dummy", "test", "sample"}:
        return get_dummy_job_description()

    headers ={
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=25)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    text = soup.get_text(separator="\n")

    cleaned = text.strip()
    if len(cleaned) < 200:
        return get_dummy_job_description()

    return cleaned
