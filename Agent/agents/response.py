from langchain.prompts import ChatPromptTemplate
from ..schemas.response import ResponseOutput
from ..llm import get_llm
from ..utils.json_guard import extract_json

llm = get_llm()

prompt = ChatPromptTemplate.from_template("""
You are a customer support email drafting agent.

Complaint:
{complaint}

Category: {category}
Sentiment: {sentiment}
Priority: {priority}

Example:
{{"subject": "...", "body": "..."}}
                                          
Rules:
- Angry → apologetic and urgent tone
- Neutral → professional tone
- Chill → friendly tone

Return valid JSON with:
- subject
- body

Do NOT include markdown.
Do NOT include extra fields.
""")

def draft_response(complaint, category, sentiment, priority) -> ResponseOutput:
    response = llm.invoke(
        prompt.format_messages(
            complaint=complaint,
            category=category,
            sentiment=sentiment,
            priority=priority
        )
    )

    clean_json = extract_json(response.content)
    return ResponseOutput.model_validate_json(clean_json)
