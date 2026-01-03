from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ComplaintResponse(BaseModel):
    id: str
    email: EmailStr
    order_id: str
    complaint_text: str
    status: str
    priority: Optional[str]
    escalation_required: bool
    email_sent: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
