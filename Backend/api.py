from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

from .db import SessionLocal, engine
from .models import Base
from .crud import create_complaint

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Complaint Ingestion API")

class ComplaintInput(BaseModel):
    email: EmailStr
    order_id: str
    complaint_text: str


@app.post("/complaints")
def submit_complaint(data: ComplaintInput):
    db = SessionLocal()
    complaint = create_complaint(
        db,
        data.email,
        data.order_id,
        data.complaint_text
    )
    db.close()

    return {
        "message": "Complaint submitted successfully",
        "complaint_id": complaint.id
    }
