from typing import Tuple


def extract_sections(generated_text: str) -> Tuple[str, str]:
    """
    Splits LLM output into short profile and cover letter blocks.
    Falls back to treating the full response as cover letter when no marker exists.
    """
    marker = "## Cover Letter"
    if marker in generated_text:
        left, right = generated_text.split(marker, 1)
        short_profile = left.strip()
        cover_letter = (marker + right).strip()
        return short_profile, cover_letter

    return "", generated_text.strip()
