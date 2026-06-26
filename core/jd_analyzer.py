"""
core/jd_analyzer.py
-------------------
Hybrid JD Analyzer (Updated for google-genai)

Pipeline:
1) Deterministic preprocessing of raw JD text
2) LLM (Gemini) extraction into STRICT schema-compliant JSON

Purpose:
Convert a Job Description into structured metadata
used downstream by matchers and scorers.
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config.settings import (
    GEMINI_MODEL_JD,
    MAX_TOKENS_JD,
    debug_log
)
from core.jd_preprocessor import preprocess_jd
from utils.json_extractor import extract_json_from_text

# Initialize client globally
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# ---------------------------------------------------------
# PROMPT CONSTRUCTION (SCHEMA-STRICT)
# ---------------------------------------------------------

def build_jd_prompt(cleaned_jd: str) -> str:
    return f"""
You are an expert technical recruiter and ATS parser.

You will be given a CLEANED job description.
Extract information strictly and conservatively.

Rules:
- Return ONLY valid JSON
- Do NOT hallucinate
- Do NOT include eligibility, visa, or degree requirements
- Skills must be concise (1–3 words)
- If unsure, leave the list empty

Return JSON in EXACTLY this structure:

{{
  "must_have_skills": [],
  "nice_to_have_skills": [],
  "responsibilities": [],
  "seniority": "entry | mid | senior"
}}

Guidelines:
- must_have_skills → explicitly required technical skills
- nice_to_have_skills → preferred or optional technical skills
- responsibilities → short action phrases (not full sentences)
- seniority → infer conservatively from language

CLEANED JOB DESCRIPTION:
{cleaned_jd}
"""


# ---------------------------------------------------------
# MAIN ANALYSIS FUNCTION
# ---------------------------------------------------------

def analyze_jd(raw_jd_text: str) -> dict:
    """
    Full JD analysis pipeline:
    1) Preprocess raw JD
    2) Send prompt to Gemini via client
    3) Extract and return validated JSON
    """
    debug_log("Starting JD analysis...")

    cleaned_jd = preprocess_jd(raw_jd_text)
    debug_log(f"Preprocessed JD (truncated): {cleaned_jd[:300]}")

    prompt = build_jd_prompt(cleaned_jd)

    # Configuration for generation
    config = types.GenerateContentConfig(
        max_output_tokens=MAX_TOKENS_JD,
        temperature=0.2
    )

    for attempt in range(2):  # retry once
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL_JD,
                contents=prompt,
                config=config
            )
            
            raw_text = response.text
            debug_log(f"Raw Gemini response (truncated): {raw_text[:200]}")

            parsed_json = extract_json_from_text(raw_text)
            debug_log("JD analysis completed successfully.")
            return parsed_json

        except Exception as e:
            debug_log(f"⚠️ JSON parse failed (attempt {attempt + 1}), retrying... Error: {e}")

    raise RuntimeError("❌ Failed to extract valid JSON from JD after retries")


# ---------------------------------------------------------
# LOCAL DEBUG RUNNER
# ---------------------------------------------------------

if __name__ == "__main__":
    """
    Local test:
    python -m core.jd_analyzer
    """
    from pprint import pprint

    sample_path = "data/samples/sample_jd.txt"
    with open(sample_path, "r", encoding="utf-8") as f:
        raw_jd = f.read()

    result = analyze_jd(raw_jd)
    pprint(result)