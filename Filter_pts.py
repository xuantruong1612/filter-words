import re
import hashlib
import os

def normalize_question(block: str) -> str:
    lines = block.strip().splitlines()
    content_lines = [line.strip() for line in lines if not re.match(r'(Question \d+|\d+(\.\.\d+)? / \d+(\.\d+)? pts)', line)]
    if not content_lines:
        return ""
    question_text = content_lines[0]
    answers = sorted(line.strip('- ').strip() for line in content_lines[1:] if line.strip())
    return question_text + '\n' + '\n'.join(answers)

def has_dash_answer(block: str) -> bool:
    return any(line.strip().startswith('-') for line in block.strip().splitlines())

def extract_question_number(block: str) -> int:
    match = re.search(r'Question\s+(\d+)', block)
    return int(match.group(1)) if match else 9999

def list_text_files() -> list[str]:
    return [f for f in os.listdir('.') if f.endswith('.txt')]

def choose_input_file() -> str:
    files = list_text_files()
    if not files:
        print("⚠️ Không có file .txt nào trong thư mục.")
        exit(1)

    print("📂 Danh sách file .txt:")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

    choice = input("🔍 Nhập số thứ tự file bạn muốn xử lý: ")
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(files):
            raise ValueError
        return files[index]
    except:
        print("❌ Lựa chọn không hợp lệ.")
        exit(1)

def ask_output_filename() -> str:
    name = input("📁 Nhập tên file output (mặc định: output.txt): ").strip()
    return name if name else "output.txt"

def remove_incorrect_and_sort(text: str) -> tuple[str, list[str]]:
    pattern = r"(Incorrect)?(Question \d+\n.*?)(?=(?:Incorrect)?Question \d+|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)

    hash_map = {}
    log_lines = []
    removed_trung = {}
    removed_incorrect = []

    for incorrect_flag, block in matches:
        block = block.strip()
        qnum = extract_question_number(block)
        if incorrect_flag:
            removed_incorrect.append((qnum, block))
            continue

        norm = normalize_question(block)
        dash = has_dash_answer(block)
        h = hashlib.md5(norm.encode('utf-8')).hexdigest()

        if h not in hash_map:
            hash_map[h] = (qnum, block, dash)
        else:
            prev_qnum, prev_block, prev_dash = hash_map[h]
            if dash and not prev_dash:
                hash_map[h] = (qnum, block, dash)
                removed_trung[prev_qnum] = (prev_block, qnum)
            elif dash == prev_dash and qnum < prev_qnum:
                hash_map[h] = (qnum, block, dash)
                removed_trung[prev_qnum] = (prev_block, qnum)
            else:
                removed_trung[qnum] = (block, prev_qnum)

    # Sắp xếp theo số cũ
    sorted_blocks_with_nums = sorted(
        [(qnum, block) for qnum, block, _ in hash_map.values()],
        key=lambda x: x[0]
    )

    # Đánh lại số và sinh log
    renumbered_blocks = []
    for new_num, (old_num, block) in enumerate(sorted_blocks_with_nums, 1):
        new_block = re.sub(r'Question\s+\d+', f'Question {new_num}', block, count=1)
        renumbered_blocks.append(new_block)
        log_lines.append(f"✅ Question {old_num} → Question {new_num}")

    if removed_incorrect:
        log_lines.append("\n❌ Câu bị loại vì 'Incorrect':")
        for num, _ in removed_incorrect:
            log_lines.append(f"❌ Question {num}")

    if removed_trung:
        log_lines.append("\n🔁 Câu bị loại vì trùng nội dung:")
        for old_qnum, (_, kept_qnum) in removed_trung.items():
            log_lines.append(f"🔁 Question {old_qnum} bị loại vì trùng với Question {kept_qnum}")

    return '\n\n'.join(renumbered_blocks), log_lines

# === Chạy chương trình ===
input_file = choose_input_file()
output_file = ask_output_filename()

# Đọc dữ liệu
with open(input_file, "r", encoding="utf-8") as f:
    raw_text = f.read()

# Xử lý
filtered, log_lines = remove_incorrect_and_sort(raw_text)

# Ghi kết quả
with open(output_file, "w", encoding="utf-8") as f:
    f.write(filtered)

# Ghi log
with open("log.txt", "w", encoding="utf-8") as logf:
    logf.write("📘 LOG CHI TIẾT XỬ LÝ CÂU HỎI\n")
    logf.write("\n".join(log_lines))
    logf.write("\n")

print(f"✅ Hoàn tất! Đã ghi kết quả vào {output_file} và log.txt.")
