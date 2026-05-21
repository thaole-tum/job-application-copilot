def write_application_draft(match_analysis: str, evidence_context: str, call_llm_fn):
    prompt = f"""
You are an expert job application writer.

Write the output in this exact structure:

## Short Profile
- 3 to 5 lines
- professional and specific
- only use skills/experience supported by evidence

## Cover Letter
Dear Hiring Team,

Paragraph 1 - Motivation for this role and this company:
- explain motivation for tasks/responsibilities and company context

Paragraph 2 - Why the candidate is a strong fit:
- map relevant skills and experience to the role requirements
- use concrete evidence from candidate background

Paragraph 3 - Closing:
- enthusiasm, contribution mindset, polite closing

Rules:
- no fake claims, no hallucinated tools/skills
- concise, confident tone
- English only

Compatibility analysis:
{match_analysis}

Retrieved evidence:
{evidence_context}
"""
    return call_llm_fn(prompt)
