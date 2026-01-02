from typing import TypedDict, Optional, List

class ComplaintState(TypedDict):
    complaint_text: str
    category: Optional[str]
    sentiment: Optional[str]
    priority: Optional[str]
    priority_reason: Optional[str]

    response_email: Optional[str]
    suggestions: Optional[List[str]]
