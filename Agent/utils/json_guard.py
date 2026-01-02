import json
import re

def extract_json(text: str) -> str:
    """
    Extract JSON from LLM responses that may contain markdown.
    """
    text = text.strip()

    # Remove ```json or ``` wrappers
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text)
        text = re.sub(r"```$", "", text)
        text = text.strip()

    # Validate JSON
    json.loads(text)
    return text
