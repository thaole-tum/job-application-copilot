def review_and_improve_draft(draft_text: str, cv_evidence: str, call_llm_fn):
    prompt = f"""
You are a strict reviewer for job application quality.

Review the draft for:
1) factual grounding in CV evidence
2) clarity and professional tone
3) structure quality for motivation + fit
4) grammar and concision

Then return:
- "## Final Draft" (improved version)
- "## Review Notes" (short bullets of what was improved)

CV evidence:
{cv_evidence}

Draft:
{draft_text}
"""
    return call_llm_fn(prompt)
