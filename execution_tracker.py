import json
import os
from datetime import datetime


def record_execution(event, details):

    os.makedirs("logs", exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "details": details
    }

    with open(
        "logs/execution_history.jsonl",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(record, ensure_ascii=False) + "\n"
        )