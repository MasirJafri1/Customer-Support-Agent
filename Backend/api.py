from fastapi import FastAPI,HTTPException,Query
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware

from .db import SessionLocal, engine
from .models import Base
from .crud import create_complaint,get_all_complaints,get_complaint_by_id,get_complaints_by_email,update_complaint,delete_complaint
from .schemas import ComplaintResponse,ComplaintUpdate
from typing import List, Optional

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Complaint Ingestion API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/complaints", response_model=List[ComplaintResponse])
def list_complaints(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None)
):
    db = SessionLocal()
    complaints = get_all_complaints(db, status, priority)
    db.close()
    return complaints


@app.get("/complaints/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: str):
    db = SessionLocal()
    complaint = get_complaint_by_id(db, complaint_id)
    db.close()

    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    return complaint


@app.patch("/complaints/{complaint_id}", response_model=ComplaintResponse)
def update_complaint_api(
    complaint_id: str,
    data: ComplaintUpdate
):
    db = SessionLocal()
    complaint = update_complaint(
        db,
        complaint_id,
        data.status,
        data.priority
    )
    db.close()

    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    return complaint


@app.delete("/complaints/{complaint_id}")
def delete_complaint_api(complaint_id: str):
    db = SessionLocal()
    success = delete_complaint(db, complaint_id)
    db.close()

    if not success:
        raise HTTPException(status_code=404, detail="Complaint not found")

    return {"message": "Complaint deleted successfully"}


@app.get(
    "/complaints/by-email/{email}",
    response_model=List[ComplaintResponse]
)
def get_complaints_for_customer(email: str):
    db = SessionLocal()
    complaints = get_complaints_by_email(db, email)
    db.close()
    return complaints
