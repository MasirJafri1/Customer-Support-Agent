from Backend.db import SessionLocal
from Backend.crud import get_new_complaints,update_complaint_result,update_complaint_status

from Agent.graph import build_graph
from FinalisingAgent.resolution import decide_resolution

app = build_graph()

def process_complaints():
    db = SessionLocal()
    complaints = get_new_complaints(db)

    print(f"Found {len(complaints)} new complaints")

    for c in complaints:
        print(f"\nProcessing complaint {c.id}")

        result = app.invoke({
            "complaint_text": c.complaint_text
        })

        priority = result.get("reevaluated_priority")
        escalated = result.get("escalation_required")

        decision = decide_resolution(
            complaint=c.complaint_text,
            priority=priority,
            escalated=escalated
        )

        if decision.auto_resolve:
            update_complaint_status(db, c.id, "resolved")
            print(f"✅ Auto-resolved: {decision.reason}")
        else:
            update_complaint_status(db, c.id, "escalated")
            print(f"🚨 Escalated: {decision.reason}")

        update_complaint_result(
            db,
            complaint_id=c.id,
            priority=priority,
            escalated=not decision.auto_resolve
        )

    db.close()
