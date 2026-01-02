from langchain.prompts import ChatPromptTemplate
from schemas.escalation import EscalationOutput
from llm import get_llm
from utils.json_guard import extract_json

llm = get_llm()

prompt = ChatPromptTemplate.from_template("""
You are an escalation decision agent.

Complaint:
{complaint}

Final Priority: {priority}
Re-evaluation Reason: {reason}

Rules:
- High priority + unresolved risk → escalate
- Legal, fraud, repeated failures → escalate
- Otherwise → no escalation

Return valid JSON with:
- escalate (true/false)
- reason

Example:
{{"escalate": true, "reason": "Payment issue unresolved"}}
""")

def decide_escalation(complaint, priority, reason):
    response = llm.invoke(
        prompt.format_messages(
            complaint=complaint,
            priority=priority,
            reason=reason
        )
    )

    clean_json = extract_json(response.content)
    return EscalationOutput.model_validate_json(clean_json)
