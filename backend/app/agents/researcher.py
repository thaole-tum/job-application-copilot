def analyze_job_context(context: str, call_llm_fn):
    prompt = f"""
You are a senior recruiter.

Analyze the retrieved job evidence and return:
1) core responsibilities
2) must-have skills
3) nice-to-have skills
4) company/team signals
5) what kind of candidate profile is ideal

Be concise and structured with bullet points.

Retrieved job evidence:
{context}
"""
    return call_llm_fn(prompt)
