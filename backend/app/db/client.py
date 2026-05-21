import datetime
import json
from pathlib import Path
from typing import Any, Dict


def save_run_payload(payload: Dict[str, Any], output_dir: str = "outputs") -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = out_dir / f"job_application_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    return file_path
