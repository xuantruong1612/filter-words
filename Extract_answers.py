import json
import os
from pathlib import Path
from typing import List

def list_available_txt_files() -> List[str]:
    return sorted([
        file for file in os.listdir('.')
        if file.lower().endswith('.txt') and os.path.isfile(file)
    ])

def choose_input_file() -> str:
    files = list_available_txt_files()
    if not files:
        print("📂 Không tìm thấy file .txt nào trong thư mục hiện tại.")
        return input("📝 Nhập tên file .txt thủ công: \n➡️  ").strip()

    print("📄 Chọn file đầu vào:")
    for i, file in enumerate(files, 1):
        print(f"  {i}. {file}")
    print(f"  {len(files) + 1}. Nhập tên file khác")

    while True:
        try:
            choice = input(f"\n➡️  Nhập lựa chọn (1-{len(files) + 1}): ").strip()
            if not choice:
                continue
            idx = int(choice)
            if 1 <= idx <= len(files):
                return files[idx - 1]
            elif idx == len(files) + 1:
                return input("📝 Nhập tên file .txt thủ công: \n➡️  ").strip()
        except:
            print("❌ Lựa chọn không hợp lệ!")

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
    input_file = choose_input_file()
    if not input_file:
        print("❌ Không có file được chọn.")
        return

    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ File '{input_file}' không tồn tại.")
        return

    output_file = "answers.json"
    text = input_path.read_text(encoding="utf-8")
    answers = extract_answers(text)
    Path(output_file).write_text(json.dumps(answers, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Đã xuất {len(answers)} đáp án đúng vào '{output_file}'")

if __name__ == "__main__":
    main()
