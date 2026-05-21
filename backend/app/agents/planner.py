def analyze_compatibility(job_analysis: str, evidence_context: str, call_llm_fn):
    prompt = f"""
You are a career coach for data/AI roles.

Task:
Evaluate compatibility between the candidate CV and job requirements.

Input:
- Job analysis
- Retrieved evidence from CV and job text

Return with clear headings:
1) Compatibility Score (0-100)
2) Strongest Matches (with evidence)
3) Missing Skills / Gaps
4) Positioning Strategy (how to present strengths honestly)

Job analysis:
{job_analysis}

Retrieved evidence:
{evidence_context}
"""
    return call_llm_fn(prompt)
