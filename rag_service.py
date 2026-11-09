from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "college_info.txt"


def retrieve_context(question):
    if not DATA_FILE.exists():
        return "College information file is not available."

    text = DATA_FILE.read_text(encoding="utf-8")

    words = re.findall(r"\w+", question.lower())
    lines = text.splitlines()

    matching_lines = []

    for line in lines:
        line_lower = line.lower()

        if any(word in line_lower for word in words):
            matching_lines.append(line)

    if matching_lines:
        return "\n".join(matching_lines)

    return text
