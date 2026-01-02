from graph import build_graph

if __name__ == "__main__":
    app = build_graph()

    complaint = {
        "complaint_text": "I ordered some books and I got some adult magazines and it has mentally disturbed my children . So I am going to sue the firm for mental harrassment."
    }

    result = app.invoke(complaint)

    print("\nFINAL STATE\n")
    for k, v in result.items():
        print(f"{k}: {v}")
