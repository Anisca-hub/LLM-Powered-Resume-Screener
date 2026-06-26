"""
utils/json_extractor.py
-----------------------
Robust JSON extractor for LLM outputs using json-repair.
"""

import json
import re
from json_repair import repair_json
from config.settings import debug_log

def extract_json_from_text(text: str) -> dict:
    if not text or not isinstance(text, str):
        raise ValueError("Empty or invalid LLM response")

    # 1. Strip markdown fences if present
    # The corrected line
    cleaned = re.sub(r"```json|```", "", text).strip()

    # 2. Use json_repair to handle truncation, missing braces, and bad formatting
    # This library is designed specifically for messy LLM outputs
    try:
        repaired_json_str = repair_json(cleaned)
        return json.loads(repaired_json_str)
    except Exception as e:
        debug_log("❌ JSON parsing failed even after repair")
        debug_log(f"Error: {e}")
        debug_log("Raw Text received:")
        debug_log(cleaned)
        raise