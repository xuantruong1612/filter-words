import re
import hashlib

def normalize_question(block: str) -> str:
    lines = block.strip().splitlines()
    content_lines = [line.strip() for line in lines if not re.match(r'(Question \d+|\d+(\.\d+)? / \d+(\.\d+)? pts)', line)]

    if not content_lines:
        return ""

    question_text = content_lines[0]
    answers = sorted(line.strip('- ').strip() for line in content_lines[1:] if line.strip())
    normalized = question_text + '\n' + '\n'.join(answers)
    return normalized

def has_dash_answer(block: str) -> bool:
    return any(line.strip().startswith('-') for line in block.strip().splitlines())

def extract_question_number(block: str) -> int:
    match = re.search(r'Question\s+(\d+)', block)
    return int(match.group(1)) if match else 9999

def renumber_questions(blocks_with_original_numbers: list[tuple[int, str]]) -> list[str]:
    """Đánh lại số và trả về danh sách block đã sửa + log"""
    renumbered_blocks = []
    log_lines = []

    for new_num, (old_num, block) in enumerate(blocks_with_original_numbers, 1):
        new_block = re.sub(r'Question\s+\d+', f'Question {new_num}', block, count=1)
        renumbered_blocks.append(new_block)
        log_lines.append(f'✅ Question {old_num} → Question {new_num}')

    return renumbered_blocks, log_lines

def remove_incorrect_and_sort(text: str) -> tuple[str, list[str]]:
    pattern = r"(Incorrect)?(Question \d+\n.*?)(?=(?:Incorrect)?Question \d+|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)

    hash_map = {}

    for incorrect_flag, block in matches:
        if incorrect_flag:
            continue

        norm = normalize_question(block)
        qnum = extract_question_number(block)
        dash = has_dash_answer(block)
        h = hashlib.md5(norm.encode('utf-8')).hexdigest()

        if h not in hash_map:
            hash_map[h] = (qnum, block.strip(), dash)
        else:
            prev_qnum, _, prev_dash = hash_map[h]
            if dash and not prev_dash:
                hash_map[h] = (qnum, block.strip(), dash)
            elif dash == prev_dash and qnum < prev_qnum:
                hash_map[h] = (qnum, block.strip(), dash)

    # Sắp xếp theo Question gốc
    sorted_blocks_with_nums = sorted(
        [(qnum, block) for qnum, block, _ in hash_map.values()],
        key=lambda x: x[0]
    )

    # Đánh lại số và sinh log
    renumbered_blocks, log_lines = renumber_questions(sorted_blocks_with_nums)
    return '\n\n'.join(renumbered_blocks), log_lines

# Đọc từ file
with open("input.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Xử lý
filtered, log_lines = remove_incorrect_and_sort(raw_text)

# Ghi ra file kết quả
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(filtered)

# Ghi log
with open("log.txt", "w", encoding="utf-8") as logf:
    logf.write("📘 Danh sách đánh số lại:\n")
    logf.write("\n".join(log_lines))
    logf.write("\n")

print("🎉 Đã lưu kết quả vào output.txt và ghi log vào log.txt.")
