from Backend.db import SessionLocal
from Backend.crud import get_new_complaints,update_complaint_result

# 🔁 Import your PHASE 3 agent
from Agent.graph import build_graph

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

        update_complaint_result(
            db,
            complaint_id=c.id,
            priority=result.get("reevaluated_priority"),
            escalated=result.get("escalation_required", False)
        )

    db.close()
