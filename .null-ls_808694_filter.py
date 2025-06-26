import re
import os

# Tên file mặc định
input_file = "input.txt"
output_file = "output.txt"
log_file = "log.txt"

# Nếu chưa có file input thì tạo file mẫu
if not os.path.exists(input_file):
    with open(input_file, "w", encoding="utf-8") as f:
        # Thêm dòng hướng dẫn vào đầu file
        f.write("📝 Ghi nội dung câu hỏi dưới đây:\n\n")
        f.write("Question 1\n0.3 / 0.3 pts\nVí dụ: Bạn thấy như thế nào?\n  Tuyệt.\n  Tuyệt2.\n")
    print(f"Đã tạo file '{input_file}'. Thêm nội dung câu hỏi vào đó rồi chạy lại.")
    exit(0)

# Đọc file
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read().strip()

if not content:
    print(f"File '{input_file}' không có nội dung.")
    exit(1)

if not re.search(r"Question \d+", content):
    print(f"❌ File '{input_file}' không chứa định dạng 'Question X'.")
    exit(1)

# Nhập từ khóa đánh dấu câu sai (sau khi đã có file)
invalid_marker = input("🔴 Nhập cụm từ đánh dấu câu sai (ví dụ: 'Incorrect' hoặc điểm '0 /'): ").strip()
print(f"❌ Từ khóa sai của bạn ➡  '{invalid_marker}'\n")

# Tách block câu hỏi
blocks = re.findall(r"(Question \d+\n[\s\S]+?)(?=Question \d+|\Z)", content)

question_header_pattern = r"Question \d+\n\d+(\.\d+)? / \d+(\.\d+)? pts\n"

seen = set()
unique_blocks = []
removed_blocks = 0
incorrect_questions = []
format_errors = []

for block in blocks:
    cleaned = re.sub(question_header_pattern, "", block).strip()

    question_number_match = re.search(r"Question (\d+)", block)
    question_number = question_number_match.group(1) if question_number_match else "?"

    # Kiểm tra đánh dấu sai
    if invalid_marker in block:
        incorrect_questions.append(f"Câu hỏi {question_number} sai")

    # Kiểm tra thiếu phương án trả lời
    if not re.search(r"\n\s{1,}[\w\-–•]", block):
        format_errors.append(f"⚠️ Câu hỏi {question_number} không có phương án trả lời.")

    # Kiểm tra trùng
    if cleaned not in seen:
        seen.add(cleaned)
        unique_blocks.append(block.strip())
    else:
        removed_blocks += 1

# Ghi output
with open(output_file, "w", encoding="utf-8") as f:
    f.write("✅ Đã lọc câu hỏi trùng lặp. Dưới đây là kết quả:\n\n")
    for i, block in enumerate(unique_blocks, 1):
        f.write(f"Câu hỏi {i}:\n{block}\n\n")

# Ghi log
with open(log_file, "w", encoding="utf-8") as log:
    log.write("📊 Thống kê:\n")
    log.write(f"    ▫️ Tổng số câu hỏi: {len(blocks)}\n")
    log.write(f"    ▫️ Câu hỏi trùng lặp đã loại bỏ: {removed_blocks}\n")
    log.write(f"    ▫️ Câu hỏi hợp lệ còn lại: {len(unique_blocks)}\n\n")

    if incorrect_questions:
        log.write(f"❌ Các câu hỏi sai (dựa trên từ khóa '{invalid_marker}'):\n")
        for q in incorrect_questions:
            log.write(f"    ▫️ {q}\n")

    if format_errors:
        log.write("\n⚠️ Lỗi định dạng:\n")
        for line in format_errors:
            log.write(f"    ▫️ {line}\n")

    if not incorrect_questions and not format_errors:
        log.write("❓Không có câu hỏi sai hoặc lỗi định dạng.\n")

print(f"✅ Đã xử lý xong. Kết quả lưu tại '{output_file}', log tại '{log_file}'.")
