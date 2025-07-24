# lọc đáp án cho vào answers.json

import json
from pathlib import Path

def extract_answers(text: str) -> dict:
    answers = {}
    current_question = 1
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("question"):
            current_question = int("".join(filter(str.isdigit, line)))
        elif line.startswith("-"):
            answer_text = line[1:].strip()
            answers[str(current_question)] = answer_text
    return answers

def main():
    input_file = input("📄 Nhập tên file đầu vào (ví dụ: input.txt): \n➡️  ").strip() or "input.txt"
    output_file = "answers.json"

    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        print(f"❌ File {input_file} không tồn tại")
        return

    text = input_path.read_text(encoding="utf-8")
    answers = extract_answers(text)
    output_path.write_text(json.dumps(answers, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Đã xuất {len(answers)} đáp án đúng vào {output_file}")

if __name__ == "__main__":
    main()
