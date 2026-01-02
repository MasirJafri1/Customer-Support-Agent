from sqlalchemy.orm import Session
from .models import Complaint

def create_complaint(db: Session, email: str, order_id: str, text: str):
    complaint = Complaint(
        email=email,
        order_id=order_id,
        complaint_text=text
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


def get_new_complaints(db: Session):
    return db.query(Complaint).filter(Complaint.status == "new").all()


def update_complaint_result(
    db: Session,
    complaint_id: str,
    priority: str,
    escalated: bool
):
    complaint = db.query(Complaint).get(complaint_id)
    complaint.priority = priority
    complaint.escalation_required = escalated
    complaint.status = "escalated" if escalated else "resolved"
    db.commit()

def update_complaint_status(
    db,
    complaint_id: str,
    status: str
):
    complaint = db.query(Complaint).get(complaint_id)
    complaint.status = status
    db.commit()

def mark_email_sent(db, complaint_id: str):
    complaint = db.query(Complaint).get(complaint_id)
    complaint.email_sent = True
    db.commit()
