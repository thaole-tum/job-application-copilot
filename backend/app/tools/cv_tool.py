from pathlib import Path

def load_cv():
    base_path = Path(__file__).parent  # folder where cv_tool.py lives
    cv_path = base_path / "my_cv.md"

    with open(cv_path, "r", encoding="utf-8") as f:
        return f.read()
