
from typing import TypedDict, Optional

class ComplaintState(TypedDict):
    complaint_text: str
    category: Optional[str]
    sentiment: Optional[str]
    priority: Optional[str]
    priority_reason: Optional[str]
