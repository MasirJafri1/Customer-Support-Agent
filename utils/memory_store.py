import json
from pathlib import Path

MEMORY_FILE = Path("memory/high_priority.json")

def store_high_priority(record: dict):
    data = json.loads(MEMORY_FILE.read_text())
    data.append(record)
    MEMORY_FILE.write_text(json.dumps(data, indent=2))
