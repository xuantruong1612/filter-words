import re
import os

input_file = "chuong1.md"

# Tự chỉnh extension file output
base_name = os.path.splitext(input_file)[0]  # Lấy tên file không có extension
current_extension = os.path.splitext(input_file)[1]  # Extension hiện tại

# Cho phép người dùng chọn extension
print(f"File input: {input_file}")
print(f"Extension hiện tại: {current_extension}")
print("\nChọn extension file output:")
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
    print("Lựa chọn không hợp lệ, giữ nguyên extension gốc")
    new_extension = current_extension

# Tạo folder và file output
output_folder = base_name  # Tạo folder với tên trùng với file input (không có extension)
output_file = os.path.join(output_folder, f"{base_name}-highlight{new_extension}")

# Tạo folder nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

print(f"Folder output: {output_folder}/")
print(f"File output: {output_file}")

# Đọc file input
try:
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
except FileNotFoundError:
    print(f"❌ Không tìm thấy file '{input_file}'")
    exit(1)

# Tách các câu hỏi: Câu hỏi X: + nội dung
blocks = re.split(r"(Câu hỏi \d+:)", content)

if not blocks or len(blocks) < 3:
    print("❌ Không tìm thấy câu hỏi hợp lệ.")
    exit(1)

result = []
processed_count = 0

for i in range(1, len(blocks), 2):
    if i + 1 >= len(blocks):
        break
        
    header = blocks[i].strip()
    body = blocks[i + 1].strip()
    
    lines = body.splitlines()
    if not lines:
        continue
    
    # Tách câu hỏi và đáp án
    # Giả sử: dòng đầu tiên là câu hỏi, các dòng còn lại là đáp án
    question_lines = [lines[0]]  # Dòng đầu tiên là câu hỏi
    answer_lines = []
    
    # Các dòng còn lại là đáp án
    for line in lines[1:]:
        line = line.strip()
        if line:  # Bỏ qua dòng trống
            answer_lines.append(line)
    
    if not answer_lines:
        print(f"⚠️ {header}: Không có đáp án")
        continue
    
    print(f"\n=== {header} ===")
    print(f"Câu hỏi: '{question_lines[0]}'")
    print("Tất cả đáp án:")
    for idx, ans in enumerate(answer_lines):
        print(f"  {idx}: '{ans}'")
    
    # Tìm đáp án đúng (có ** hoặc bắt đầu bằng dấu -)
    correct_answer = None
    correct_index = -1
    
    for idx, ans in enumerate(answer_lines):
        # Kiểm tra đáp án đúng: có **- hoặc bắt đầu bằng -
        if "**-" in ans or "**–" in ans or "**•" in ans or ans.startswith(("-", "–", "•")):
            print(f"  -> Tìm thấy đáp án đúng: '{ans}'")
            # Đảm bảo có format **text**
            if not ans.startswith("**"):
                correct_answer = f"**{ans}**"
            else:
                correct_answer = ans
            correct_index = idx
            break
    
    # Sắp xếp lại đáp án
    if correct_answer is not None and correct_index >= 0:
        print(f"Đưa đáp án đúng lên đầu: '{correct_answer}'")
        # Xóa khỏi vị trí cũ
        answer_lines.pop(correct_index)
        # Thêm vào đầu
        answer_lines.insert(0, correct_answer)
        print("Thứ tự mới:")
        for idx, ans in enumerate(answer_lines):
            print(f"  {idx}: '{ans}'")
    else:
        print("❌ Không tìm thấy đáp án đúng!")
    
    # Ghép lại thành block hoàn chỉnh
    full_block = [header] + question_lines + answer_lines
    result.append("\n".join(full_block))
    processed_count += 1

# Ghi file kết quả
if result:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(result))
    print(f"\n✅ Đã xử lý {processed_count} câu hỏi hoàn tất.")
    print(f"✅ Kết quả nằm trong '{output_file}'")
else:
    print("❌ Không có câu hỏi nào được xử lý.")
