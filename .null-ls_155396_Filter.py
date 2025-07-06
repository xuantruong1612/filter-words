import re
import os

input_file = "Input.txt"
log_file = "log.txt"

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
