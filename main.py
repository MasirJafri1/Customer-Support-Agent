from graph import build_graph

if __name__ == "__main__":
    app = build_graph()

    complaint = {
        "complaint_text": "The quality of the product can be done more better."
    }

    result = app.invoke(complaint)

    print("\nFINAL OUTPUT\n")
    for k, v in result.items():
        print(f"{k}: {v}")
