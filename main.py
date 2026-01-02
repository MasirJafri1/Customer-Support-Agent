from graph import build_graph

if __name__ == "__main__":
    app = build_graph()

    complaint = {
        "complaint_text": "Material quality below average n you just fooling people by showing big discount which is pure cheat"
    }

    result = app.invoke(complaint)

    print("\nFINAL OUTPUT\n")
    for k, v in result.items():
        print(f"{k}: {v}")
