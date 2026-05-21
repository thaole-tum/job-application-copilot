from app.agents import (
    analyze_compatibility,
    analyze_job_context,
    review_and_improve_draft,
    write_application_draft,
)
from app.db.client import save_run_payload
from app.llm.client import call_llm
from app.rag import SimpleRAGRetriever, format_context_blocks
from app.tools.cover_letter_tool import extract_sections
from app.tools.cv_tool import load_cv
from app.tools.job_parser import scrape_job


def build_application(job_url: str):
    job_text = scrape_job(job_url)
    cv_text = load_cv()

    retriever = SimpleRAGRetriever(chunk_size=900, overlap=150)
    retriever.add_document("job_description", job_text)
    retriever.add_document("cv", cv_text)

    analysis_context = format_context_blocks(
        retriever.retrieve(
            "job requirements responsibilities key skills ideal candidate profile",
            top_k=4,
        )
    )
    job_analysis = analyze_job_context(analysis_context, call_llm)

    match_context = format_context_blocks(
        retriever.retrieve(
            f"{job_analysis}\ncompatibility missing skills strongest matches CV evidence",
            top_k=5,
        )
    )
    compatibility_analysis = analyze_compatibility(job_analysis, match_context, call_llm)

    writing_context = format_context_blocks(
        retriever.retrieve(
            f"{compatibility_analysis}\nwrite profile and cover letter based on CV-backed evidence only",
            top_k=5,
        )
    )
    draft = write_application_draft(compatibility_analysis, writing_context, call_llm)
    final_result = review_and_improve_draft(draft, cv_text[:7000], call_llm)

    short_profile, cover_letter = extract_sections(final_result)

    payload = {
        "job_url": job_url,
        "job_analysis": job_analysis,
        "compatibility_analysis": compatibility_analysis,
        "short_profile": short_profile,
        "cover_letter": cover_letter,
        "final_result": final_result,
    }
    output_path = save_run_payload(payload)
    print(f"\nSaved structured output to: {output_path}")

    return final_result
