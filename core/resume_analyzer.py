"""
core/resume_analyzer.py
-----------------------
Chunked Resume Analyzer (PRODUCTION SAFE - Updated for google-genai)
"""
import time
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config.settings import GEMINI_MODEL_RESUME, MAX_TOKENS_RESUME, debug_log
from utils.json_extractor import extract_json_from_text
from utils.helpers import split_resume_into_sections

# Initialize client globally
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def build_resume_prompt(section_name: str, section_text: str) -> str:
    return f"""
You are an expert technical resume reviewer.
You are analyzing ONLY this resume section: {section_name}

Rules:
- Return ONLY valid JSON
- DO NOT hallucinate
- ONLY include skills with CLEAR evidence in this section
- Skills must be concise (1–3 words)

Return JSON in EXACTLY this structure:
{{
  "skills_with_evidence": {{
    "skill_name": ["evidence"]
  }},
  "projects": [],
  "tools": []
}}

SECTION TEXT:
{section_text}
"""

def analyze_resume(resume_text: str) -> dict:
    debug_log("Starting chunked resume analysis...")

    # 🔒 SAFETY GUARD
    if isinstance(resume_text, dict):
        resume_text = resume_text.get("text", "") or ""

    if not isinstance(resume_text, str):
        raise TypeError(f"analyze_resume expected str, got {type(resume_text)}")

    sections = split_resume_into_sections(resume_text)

    final = {
        "skills_with_evidence": {},
        "projects": [],
        "tools": []
    }

    # Configuration for generation
    config = types.GenerateContentConfig(
        max_output_tokens=MAX_TOKENS_RESUME,
        temperature=0.2
    )

    for section_name, section_text in sections.items():
        if len(section_text.strip()) < 50:
            continue
    
        # 2. Add this sleep statement to wait 15 seconds between chunks
        time.sleep(15) 
        
        prompt = build_resume_prompt(section_name, section_text)

        # Updated call using the client
        response = client.models.generate_content(
            model=GEMINI_MODEL_RESUME,
            contents=prompt,
            config=config
        )

        raw = response.text
        print(raw)
        parsed = extract_json_from_text(raw)

        # --- merge safely ---
        for skill, ev in parsed.get("skills_with_evidence", {}).items():
            final["skills_with_evidence"].setdefault(skill, []).extend(ev)

        final["projects"].extend(parsed.get("projects", []))
        final["tools"].extend(parsed.get("tools", []))

    debug_log("Resume analysis completed successfully.")
    return final