import re
import os

input_file = "Input.txt"
log_file = "Log.txt"

# Tạo file input mẫu nếu chưa có
if not os.path.exists(input_file):
    with open(input_file, "w", encoding="utf-8") as f:
        f.write("📝 Ghi nội dung câu hỏi dưới đây:\n\n")
        f.write("Question 1\n0.3 / 0.3 pts\nVí dụ: Bạn thấy như thế nào?\n  Tuyệt.\n  Tuyệt2.\n")
    print(f"Đã tạo file '{input_file}'. Thêm nội dung câu hỏi vào đó rồi chạy lại.")
    exit(0)

# Đọc nội dung file
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read().strip()

if not content:
    print(f"File '{input_file}' không có nội dung.")
    exit(1)

# 💡 Fix định dạng lỗi
content = re.sub(r"(?<!\n)(Question \d+)", r"\n\1", content)
content = re.sub(r"(Incorrect)(Question \d+)", r"\1\n\2", content)

# Kiểm tra có chứa 'pts'
if not re.search(r"pts\n", content):
    print(f"❌ File '{input_file}' không chứa định dạng điểm '... pts'.")
    exit(1)

# ✅ Lúc này mới hỏi tên file output
print("📝 Nhập tên file output:")
output_filename = input("Tên file của bạn + tên đuôi bạn muốn (ví dụ: 'chuong1.txt' hoặc 'bai-tap.docx'): \nNhập: ").strip()

if '.' not in output_filename:
    print(f"⚠️ Tên file '{output_filename}' không có đuôi mở rộng!")
    print("Bạn muốn:")
    print("  1. Nhập lại tên file + đuôi")
    print("  2. Thoát chương trình")
    
    while True:
        choice = input("Chọn 1 hoặc 2: ").strip().lower()
        if choice in ['1', 'yes', 'y']:
            output_filename = input("Nhập tên file + đuôi: ").strip()
            if '.' not in output_filename:
                print("❌ Vẫn chưa có đuôi file! Vui lòng nhập lại.")
                continue
            else:
                print(f"✅ Tên file output: '{output_filename}'")
                break
        elif choice in ['2', 'no', 'n']:
            print("\n👋 Bái bai!\n")
            exit(0)
        else:
            print("❌ Vui lòng chọn 1 hoặc 2\n  1. Nhập lại tên file + đuôi(ví dụ .txt)\n  2. Thoát")
else:
    print(f"✅ Tên file output: '{output_filename}'")

output_file = output_filename

# 🔴 Nhập từ khóa đánh dấu sai
invalid_marker = input("🔴 Nhập cụm từ đánh dấu câu sai (ví dụ: 'Incorrect' hoặc điểm '0 /'): ").strip()
if not invalid_marker:
    invalid_marker = "0 /"
print(f"❌ Từ khóa sai của bạn ➡  '{invalid_marker}'\n")

# Tách các block câu hỏi từ content
pattern = r"(Question \d+\n\d+(?:\.\d+)? / \d+(?:\.\d+)? pts\n([\s\S]+?))(?=Question \d+\n\d+(?:\.\d+)? / \d+(?:\.\d+)? pts\n|\Z)"
matches = re.findall(pattern, content)

seen_questions = set()
unique_blocks = []
removed_blocks = 0
incorrect_questions = set()
format_errors = []

for full_block, after_pts in matches:
    lines = after_pts.strip().splitlines()
    question_text_only = lines[0].strip() if lines else ""
    question_number_match = re.search(r"Question (\d+)", full_block)
    question_number = question_number_match.group(1) if question_number_match else "?"

    # Kiểm tra câu sai
    is_incorrect = invalid_marker in full_block or "Incorrect" in full_block
    if is_incorrect:
        if question_number != "?":
            incorrect_questions.add(f"Câu hỏi {int(question_number):02} sai")
        else:
            incorrect_questions.add("Câu hỏi không rõ số bị sai")

    # Kiểm tra định dạng có đáp án
    if len(lines) < 2 or not re.search(r"\s{1,}[\w\-–•]", lines[1]):
        format_errors.append(f"⚠️ Câu hỏi {question_number} không có phương án trả lời.")

    # Lọc trùng và bỏ qua câu sai
    if question_text_only not in seen_questions and not is_incorrect:
        seen_questions.add(question_text_only)
        unique_blocks.append((question_number, after_pts.strip()))
    elif question_text_only in seen_questions:
        removed_blocks += 1

# Ghi output
with open(output_file, "w", encoding="utf-8") as f:
    f.write("✅ Đã lọc câu hỏi trùng lặp (theo nội dung câu hỏi).\nKết quả:\n\n")
    for i, (q_num, content_after_pts) in enumerate(unique_blocks, 1):
        f.write(f"Câu hỏi {q_num}:\n{content_after_pts}\n\n")

# Ghi log
with open(log_file, "w", encoding="utf-8") as log:
    log.write("📊 Thống kê:\n")
    log.write(f"    ▫️ Tổng số câu hỏi phát hiện: {len(matches)}\n")
    log.write(f"    ▫️ Câu hỏi trùng lặp (cùng nội dung): {removed_blocks}\n")
    log.write(f"    ▫️ Câu hỏi hợp lệ còn lại: {len(unique_blocks)}\n\n")

    if incorrect_questions:
        log.write(f"❌ Câu hỏi sai (từ khóa '{invalid_marker}'):\n")
        for q in sorted(incorrect_questions):
            log.write(f"    ▫️ {q}\n")

    if format_errors:
        log.write("\n⚠️ Cảnh báo định dạng:\n")
        for line in format_errors:
            log.write(f"    ▫️ {line}\n")

    if not incorrect_questions and not format_errors:
        log.write("✅ Không có câu hỏi sai hoặc lỗi định dạng.\n")

print(f"\n✅ Đã xử lý xong. Kết quả lưu tại '{output_file}', log tại '{log_file}'.")
