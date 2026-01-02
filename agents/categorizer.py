from langchain.prompts import ChatPromptTemplate
from schemas.category import CategoryOutput
from llm import get_llm
from utils.json_guard import extract_json


llm = get_llm()

prompt = ChatPromptTemplate.from_template("""
You are a customer support categorization agent.

Complaint:
{complaint}

Classify into one of:
- payment_issue
- delivery_issue
- technical_issue
- feedback
- other

Return ONLY valid JSON.
""")

def categorize(complaint: str) -> CategoryOutput:
    response = llm.invoke(
        prompt.format_messages(complaint=complaint)
    )
    clean_json = extract_json(response.content)
    return CategoryOutput.model_validate_json(clean_json)

