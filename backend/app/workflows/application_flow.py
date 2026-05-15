from app.tools.job_parser import scrape_job
from app.tools.cv_tool import load_cv
from app.llm.client import call_llm

def build_application(job_url: str):
    job_text = scrape_job(job_url)
    cv_text = load_cv()

    prompt_analysis = f"""
You are a professional recruiter in Germany.

Goal: Analyze this job:

{job_text[:6000]}

Extract:
- key skills
- responsibilities
- ideal candidate profile
"""

    job_analysis = call_llm(prompt_analysis)

    prompt_match = f"""
You are a professional tech career coach in the field of data science, data analytics, AI, Machine Learning, Business Analyst.

Goal: Compare CV and job to see the compatibility.

JOB:
{job_analysis}

CV:
{cv_text}

Return:
1. compatibility score (0-100)
2. missing skills
3. strongest matches
"""

    match = call_llm(prompt_match)

    prompt_output = f"""
Based on this analysis:

{match}

And this CV:
{cv_text}

Write:
1. Short professional self-introduction profile in english (3-5 lines)
2. Cover letter in English (concise, tailored) and based the compatable skills and experiences in the CV with the core skills in the job description.

Rule: Do not hallucinate and generate fake skills that are not mentioned in the CV.
"""

    result = call_llm(prompt_output)

    os.makedirs("outputs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"outputs/job_application_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"\n✅ Saved output to: {filename}")

    return result 
