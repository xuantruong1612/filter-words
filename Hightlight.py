# tạo file tô đậm đáp án, cho đáp án đúng lên đầu

import re
import os

def is_valid_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return bool(re.search(r"Câu hỏi \d+:", content))
    except:
        return False

# Quét các file hợp lệ trong thư mục hiện tại
all_files = [f for f in os.listdir() if os.path.isfile(f)]
valid_files = [f for f in all_files if is_valid_file(f)]

if not valid_files:
    print("❌ Không tìm thấy file hợp lệ trong thư mục.")
    exit(1)

# Hiển thị danh sách file cho người dùng chọn
print("📄 Danh sách file hợp lệ:")
for idx, file in enumerate(valid_files, start=1):
    print(f"{idx}. {file}")

# Người dùng chọn file
while True:
    try:
        choice = int(input("\n➡️ Nhập số tương ứng với file muốn xử lý: "))
        if 1 <= choice <= len(valid_files):
            input_file = valid_files[choice - 1]
            break
        else:
            print("⚠️ Số không hợp lệ. Vui lòng chọn lại.")
    except ValueError:
        print("⚠️ Vui lòng nhập số.")

# Lấy tên file và đuôi mở rộng
base_name = os.path.splitext(input_file)[0]
current_extension = os.path.splitext(input_file)[1]

# Cho phép chọn extension output
print(f"\n📂 File input: {input_file}")
print(f"📎 Extension hiện tại: {current_extension}")
print("\nChọn định dạng file output:")
print("1. .txt")
print("2. .md")
print("3. .docx")
print("4. .html")
print("5. Giữ nguyên extension gốc")
print("6. Tự nhập")

choice = input("Nhập lựa chọn (1-6): ").strip()

if choice == "1":
    new_extension = ".txt"
elif choice == "2":
    new_extension = ".md"
elif choice == "3":
    new_extension = ".docx"
elif choice == "4":
    new_extension = ".html"
elif choice == "5":
    new_extension = current_extension
elif choice == "6":
    custom_extension = input("Nhập extension tùy chỉnh (ví dụ: .pdf): ").strip()
    if not custom_extension.startswith("."):
        custom_extension = "." + custom_extension
    new_extension = custom_extension
else:
    print("⚠️ Lựa chọn không hợp lệ, giữ nguyên extension gốc.")
    new_extension = current_extension

# Chuẩn bị đường dẫn output
output_folder = base_name
output_file = os.path.join(output_folder, f"{base_name}-highlight{new_extension}")
os.makedirs(output_folder, exist_ok=True)

print(f"\n📁 Thư mục output: {output_folder}/")
print(f"📝 File output: {output_file}")

# Đọc nội dung file input
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read().strip()

# Phân tích và xử lý
blocks = re.split(r"(Câu hỏi \d+:)", content)

if not blocks or len(blocks) < 3:
    print("❌ Không tìm thấy câu hỏi hợp lệ.")
    exit(1)

result = []
processed_count = 0
is_markdown = new_extension.lower() == ".md"

for i in range(1, len(blocks), 2):
    if i + 1 >= len(blocks):
        break

    header = blocks[i].strip()
    body = blocks[i + 1].strip()
    lines = body.splitlines()
    if not lines:
        continue

    question_lines = [lines[0]]
    answer_lines = [line.strip() for line in lines[1:] if line.strip()]
    
    correct_answer = None
    correct_index = -1
    for idx, ans in enumerate(answer_lines):
        if ans.startswith(("-", "–", "•")):
            correct_answer = ans
            correct_index = idx
            break

    if correct_answer is not None and correct_index >= 0:
        answer_lines.pop(correct_index)
        highlighted = f"**{correct_answer}**" if is_markdown else correct_answer
        answer_lines.insert(0, highlighted)

    full_block = [header] + question_lines + answer_lines
    result.append("\n".join(full_block))
    processed_count += 1

if result:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(result))
    print(f"\n✅ Đã xử lý {processed_count} câu hỏi.")
    print(f"📌 Kết quả lưu tại: {output_file}")
else:
    print("❌ Không có câu hỏi nào được xử lý.")
