# Lọc đáp án trong file nhưng có pts - Cải tiến ưu tiên dấu "-"

import re
import os
import json
import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Set

class QuestionFilter:
    def __init__(self):
        self.default_input_file = "Input.txt"
        self.input_file = ""
        self.log_file = "Log.txt"
        self.config_file = "config.json"
        self.backup_dir = "backups"

    def list_available_files(self) -> List[str]:
        supported_extensions = ['.txt', '.docx', '.doc']
        return sorted([
            file for file in os.listdir('.')
            if any(file.lower().endswith(ext) for ext in supported_extensions)
            and os.path.isfile(file)
        ])

    def get_input_file(self) -> str:
        print("📁 Chọn file input:")
        print("=" * 30)
        files = self.list_available_files()

        if files:
            for i, file in enumerate(files, 1):
                size = os.path.getsize(file)
                size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
                print(f"  ▫️  {i}. {file} ({size_str})")
            print(f"  ▫️  {len(files) + 1}. Nhập tên file khác")
            print(f"  ▫️  {len(files) + 2}. Tạo file '{self.default_input_file}' mẫu")

            while True:
                try:
                    choice = input(f"\nChọn (1-{len(files) + 2}): ").strip()
                    if not choice: continue
                    n = int(choice)
                    if 1 <= n <= len(files):
                        return files[n - 1]
                    elif n == len(files) + 1:
                        return self.get_custom_input_filename()
                    elif n == len(files) + 2:
                        self.create_sample_input()
                        return ""
                except KeyboardInterrupt:
                    print("\n👋 Thoát chương trình!"); exit(0)
                except:
                    print("❌ Lựa chọn không hợp lệ!")
        else:
            print("📂 Không tìm thấy file nào!")
            print("1. Nhập tên file")
            print(f"2. Tạo file '{self.default_input_file}' mẫu")
            choice = input("Chọn (1/2): ").strip()
            return self.get_custom_input_filename() if choice == '1' else (self.create_sample_input() or "")

    def get_custom_input_filename(self) -> str:
        while True:
            filename = input("📝 Nhập tên file input (có đuôi .txt): \n➡️  ").strip()
            if not filename: continue
            if '.' not in filename:
                filename += '.txt'
                print(f"🔧 Tự động thêm đuôi: {filename}")
            if not os.path.exists(filename):
                ch = input("1. Nhập lại | 2. Tạo file mới | 3. Thoát (1/2/3): ").strip()
                if ch == '2':
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write("📝 Ghi nội dung câu hỏi dưới đây:\n\nQuestion 1\n0.3 / 0.3 pts\nVí dụ: Bạn thấy sao?\n  Tuyệt.\n  Tuyệt2.\n")
                    return ""
                elif ch == '3':
                    exit(0)
                else:
                    continue
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    _ = f.read(100)
                return filename
            except:
                print(f"❌ Không thể đọc file '{filename}'")
                continue

    def create_sample_input(self) -> None:
        try:
            with open(self.default_input_file, "w", encoding="utf-8") as f:
                f.write("Question 1\n0.3 / 0.3 pts\nVí dụ: Bạn thấy sao?\n  Tuyệt.\n  Tuyệt2.\n\n")
                f.write("Question 2\n0.5 / 0.5 pts\nCâu hỏi thứ hai:\n  Đáp án A\n  Đáp án B\n  Đáp án C\n\n")
                f.write("Question 3\nIncorrect\n0 / 0.5 pts\nCâu sai:\n  Sai A\n  Sai B\n")
        except Exception as e:
            print(f"❌ Lỗi tạo file mẫu: {e}")

    def backup_file(self, filename: str) -> str:
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{self.backup_dir}/{Path(filename).stem}_{timestamp}{Path(filename).suffix}"
            with open(filename, 'r', encoding='utf-8') as src, open(backup_name, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            return backup_name
        except:
            return ""

    def load_config(self) -> Dict:
        default = {
            "invalid_markers": ["Incorrect", "0 /", "0.0 /"],
            "output_formats": [".txt", ".docx", ".json", ".csv"],
            "auto_backup": True,
            "last_input_file": "",
            "renumber_questions": True
        }
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return {**default, **json.load(f)}
        except:
            pass
        return default

    def save_config(self, config: Dict) -> None:
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except:
            pass

    def read_input_file(self, filename: str) -> str:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return f.read().strip()
        except UnicodeDecodeError:
            with open(filename, "r", encoding="cp1252") as f:
                return f.read().strip()
        except:
            return ""

    def fix_content_format(self, content: str) -> str:
        fixes = [
            (r"(?<!\n)(Question \d+)", r"\n\1"),
            (r"(Incorrect)(Question \d+)", r"\1\n\2"),
            (r"(\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?\s*pts)([^\n])", r"\1\n\2"),
            (r"\n\s*\n\s*\n", r"\n\n")
        ]
        for pat, rep in fixes:
            content = re.sub(pat, rep, content)
        return content

    def validate_content(self, content: str) -> Tuple[bool, List[str]]:
        errors = []
        if not content:
            return False, ["File rỗng"]
        if not re.search(r"\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?\s*pts", content):
            errors.append("Không có định dạng điểm '... pts'")
        if not re.findall(r"Question \d+", content):
            errors.append("Không có câu hỏi 'Question X'")
        return (len(errors) == 0), errors

    def get_output_filename(self, config: Dict) -> str:
        print("📝 Nhập tên file output:")
        while True:
            filename = input("Tên file + đuôi (vd: output.txt): ").strip()
            if '.' not in filename:
                print("⚠️ Thiếu đuôi file!")
                continue
            ext = Path(filename).suffix.lower()
            if ext not in config["output_formats"]:
                print(f"❌ Không hỗ trợ '{ext}'")
                continue
            return filename

    def get_invalid_markers(self, config: Dict) -> List[str]:
        print(f"🔴 Từ khóa sai: {config['invalid_markers']}")
        use_default = input("Dùng mặc định? (y/n): ").strip().lower()
        if use_default in ['n', 'no']:
            markers = input("Nhập từ khóa (phân tách bởi dấu phẩy): ").strip()
            if markers:
                return [m.strip() for m in markers.split(',')]
        return config['invalid_markers']

    def get_sort_preference(self, config: Dict) -> bool:
        """Hỏi người dùng có muốn đánh số lại từ 1 không"""
        current = "có" if config.get("renumber_questions", True) else "không"
        print(f"🔢 Đánh số lại từ Question 1, 2, 3... (hiện tại: {current})")
        choice = input("Đánh số lại từ 1? (y/n): ").strip().lower()
        if choice in ['n', 'no']:
            return False
        return True

    def normalize_question_for_comparison(self, text: str) -> str:
        text = text.strip()
        return re.sub(r'^[-–•\s]+', '', text).strip()

    def parse_questions(self, content: str) -> List[Tuple[str, str]]:
        pattern = r"(Question\s+(\d+)\n[\s\S]+?)(?=Question\s+\d+\n|\Z)"
        return [(m[1], m[0].split('\n', 1)[1].strip()) for m in re.findall(pattern, content)]

    def sort_questions_by_number(self, questions: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """Sắp xếp câu hỏi theo số thứ tự"""
        def get_question_number(question_tuple):
            try:
                return int(question_tuple[0])
            except ValueError:
                # Nếu không parse được số, đặt ở cuối
                return float('inf')
        
        return sorted(questions, key=get_question_number)

    def filter_questions(self, questions: List[Tuple[str, str]], invalid_markers: List[str], renumber: bool = True) -> Dict:
        # Thu thập tất cả câu hỏi theo nội dung chuẩn hóa
        content_groups: Dict[str, List[Tuple[str, str, str, bool]]] = {}  # norm_content -> [(num, body, q_text, has_dash)]
        incorrect: Set[str] = set()

        # Sắp xếp câu hỏi theo số thứ tự trước khi xử lý
        questions = self.sort_questions_by_number(questions)

        # Bước 1: Thu thập tất cả câu hỏi và nhóm theo nội dung
        for num, body in questions:
            lines = body.splitlines()
            q_text = lines[1].strip() if len(lines) >= 2 else ""
            
            # Bỏ qua câu hỏi sai
            if any(m in body for m in invalid_markers):
                incorrect.add(f"Question {num}")
                continue
            
            # Chuẩn hóa nội dung để so sánh
            norm_content = self.normalize_question_for_comparison(q_text)
            
            # Kiểm tra xem có đáp án bắt đầu bằng dấu "-" không
            has_dash_answers = any(line.strip().startswith('-') for line in lines[2:] if line.strip())
            
            # Thêm vào nhóm
            if norm_content not in content_groups:
                content_groups[norm_content] = []
            content_groups[norm_content].append((num, body, q_text, has_dash_answers))

        # Bước 2: Chọn câu tốt nhất từ mỗi nhóm
        selected_questions = []
        dup_info = []
        removed = 0

        for norm_content, group in content_groups.items():
            if len(group) == 1:
                # Không có trùng lặp
                num, body, q_text, has_dash = group[0]
                selected_questions.append((num, body, q_text))
            else:
                # Có trùng lặp - chọn câu tốt nhất
                removed += len(group) - 1
                
                # Phân loại câu trong nhóm
                dash_questions = [(num, body, q_text, has_dash) for num, body, q_text, has_dash in group if has_dash]
                non_dash_questions = [(num, body, q_text, has_dash) for num, body, q_text, has_dash in group if not has_dash]
                
                # LOGIC SỬA: Ưu tiên tuyệt đối câu có dấu "-"
                if dash_questions:
                    # Có câu với dấu "-", chọn câu có số nhỏ nhất trong nhóm này
                    best = min(dash_questions, key=lambda x: int(x[0]) if x[0].isdigit() else float('inf'))
                    selected_questions.append((best[0], best[1], best[2]))
                    
                    # Ghi log về các câu bị loại (bao gồm cả câu không có dấu "-")
                    all_numbers = [q[0] for q in group]
                    rejected_numbers = [q[0] for q in group if q[0] != best[0]]
                    
                    dash_rejected = [q[0] for q in dash_questions if q[0] != best[0]]
                    non_dash_rejected = [q[0] for q in non_dash_questions]
                    
                    log_msg = f"Nhóm trùng {all_numbers} → chọn Q{best[0]} (có dấu '-')"
                    if dash_rejected:
                        log_msg += f", loại Q{dash_rejected} (cũng có '-' nhưng số lớn hơn)"
                    if non_dash_rejected:
                        log_msg += f", loại Q{non_dash_rejected} (không có '-')"
                    
                    dup_info.append(log_msg)
                    
                else:
                    # Không có câu nào có dấu "-", chọn câu có số nhỏ nhất
                    best = min(non_dash_questions, key=lambda x: int(x[0]) if x[0].isdigit() else float('inf'))
                    selected_questions.append((best[0], best[1], best[2]))
                    
                    # Ghi log về các câu bị loại
                    all_numbers = [q[0] for q in group]
                    rejected_numbers = [q[0] for q in group if q[0] != best[0]]
                    dup_info.append(f"Nhóm trùng {all_numbers} → chọn Q{best[0]} (số nhỏ nhất, không có câu nào có '-'), loại: {rejected_numbers}")

        # Bước 3: Sắp xếp kết quả và xử lý trùng số
        unique_blocks = []
        seen_numbers: Dict[str, int] = {}
        number_conflicts = []
        
        # Sắp xếp lại theo số thứ tự gốc
        selected_questions.sort(key=lambda x: int(x[0]) if x[0].isdigit() else float('inf'))
        
        for num, body, q_text in selected_questions:
            # Kiểm tra trùng số Question (chỉ khi không đánh số lại)
            if not renumber and num in seen_numbers:
                original_num = num
                counter = 1
                while f"{num}_{counter}" in seen_numbers or num in seen_numbers:
                    counter += 1
                new_num = f"{original_num}_{counter}"
                number_conflicts.append(f"Question {original_num} trùng số → đổi thành Question {new_num}")
                num = new_num
            
            if not renumber:
                seen_numbers[num] = 1
            unique_blocks.append((num, body, q_text))

        # Bước 4: Đánh số lại từ 1 nếu được yêu cầu
        if renumber:
            print("🔢 Đánh số lại từ Question 1, 2, 3...")
            renumbered_blocks = []
            for i, (old_num, body, q_text) in enumerate(unique_blocks, 1):
                renumbered_blocks.append((str(i), body, q_text))
            unique_blocks = renumbered_blocks

        return {
            'unique_blocks': unique_blocks,
            'removed_blocks': removed,
            'incorrect_questions': incorrect,
            'format_errors': [],
            'total_questions': len(questions),
            'duplicate_info': dup_info,
            'number_conflicts': number_conflicts,
            'renumbered': renumber
        }

    def _write_text(self, filename: str, data: Dict) -> None:
        """Ghi file text - giữ nguyên định dạng ban đầu"""
        with open(filename, "w", encoding="utf-8") as f:
            for q_num, content, _ in data['unique_blocks']:
                f.write(f"Question {q_num}\n{content}\n\n")

    def write_output(self, filename: str, data: Dict) -> None:
        ext = Path(filename).suffix.lower()
        if ext == '.json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif ext == '.csv':
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Question_ID', 'Content'])
                for q_num, content, _ in data['unique_blocks']:
                    writer.writerow([q_num, content.replace('\n', ' | ')])
        else:
            self._write_text(filename, data)

    def write_log(self, data: Dict, markers: List[str]) -> None:
        try:
            with open(self.log_file, "w", encoding="utf-8") as log:
                log.write(f"📊 Xử lý lúc {datetime.datetime.now()}\n")
                log.write(f"Tổng: {data['total_questions']}, Hợp lệ: {len(data['unique_blocks'])}, Loại: {data['removed_blocks'] + len(data['incorrect_questions'])}\n")
                
                if data['incorrect_questions']:
                    log.write("❌ Câu sai:\n" + "\n".join(f"  - {q}" for q in data['incorrect_questions']) + "\n")
                
                if data['duplicate_info']:
                    log.write("🔁 Câu trùng nội dung:\n" + "\n".join(f"  - {info}" for info in data['duplicate_info']) + "\n")
                
                # Thêm thông tin về xung đột số Question
                if data.get('number_conflicts'):
                    log.write("⚠️ Xung đột số Question:\n" + "\n".join(f"  - {conflict}" for conflict in data['number_conflicts']) + "\n")
                
                # Thêm thông tin về thứ tự câu hỏi đã được sắp xếp
                log.write("📋 Thứ tự câu hỏi trong output:\n")
                for i, (q_num, _, q_text) in enumerate(data['unique_blocks'], 1):
                    log.write(f"  {i}. Question {q_num}: {q_text[:50]}{'...' if len(q_text) > 50 else ''}\n")
                
                # Thêm thống kê về dấu "-"
                dash_count = 0
                for q_num, body, q_text in data['unique_blocks']:
                    lines = body.splitlines()
                    if any(line.strip().startswith('-') for line in lines[2:] if line.strip()):
                        dash_count += 1
                
                log.write(f"\n📊 Thống kê dấu '-': {dash_count}/{len(data['unique_blocks'])} câu có đáp án dạng '-'\n")
        except:
            pass

    def run(self) -> None:
        print("🔍 Lọc câu hỏi trùng & sai (Ưu tiên dấu '-')")
        config = self.load_config()
        self.input_file = self.get_input_file()
        if not self.input_file:
            return
        config['last_input_file'] = self.input_file
        
        if config.get("auto_backup", True):
            bkup = self.backup_file(self.input_file)
            if bkup:
                print(f"📦 Backup: {bkup}")
        
        content = self.read_input_file(self.input_file)
        if not content: return
        
        is_valid, errs = self.validate_content(content)
        if not is_valid:
            print("❌ Lỗi:\n" + "\n".join(f"  - {e}" for e in errs))
            return
        
        content = self.fix_content_format(content)
        output = self.get_output_filename(config)
        markers = self.get_invalid_markers(config)
        
        # Hỏi về việc đánh số lại
        renumber = self.get_sort_preference(config)
        config['renumber_questions'] = renumber
        self.save_config(config)
        
        print("⏳ Đang xử lý...")
        questions = self.parse_questions(content)
        data = self.filter_questions(questions, markers, renumber)
        
        print(f"📊 Tổng: {data['total_questions']}, Giữ: {len(data['unique_blocks'])}, Loại: {data['removed_blocks'] + len(data['incorrect_questions'])}")
        
        # Hiển thị thống kê dấu "-"
        dash_count = 0
        for q_num, body, q_text in data['unique_blocks']:
            lines = body.splitlines()
            if any(line.strip().startswith('-') for line in lines[2:] if line.strip()):
                dash_count += 1
        print(f"🎯 Câu có dấu '-': {dash_count}/{len(data['unique_blocks'])}")
        
        # Hiển thị thông tin xung đột số Question nếu có
        if data.get('number_conflicts') and not data.get('renumbered'):
            print("⚠️ Phát hiện trùng số Question:")
            for conflict in data['number_conflicts']:
                print(f"  - {conflict}")
        
        # Hiển thị preview thứ tự câu hỏi
        if data['unique_blocks']:
            mode_desc = "đánh số lại từ 1" if data.get('renumbered') else "giữ số gốc"
            print(f"📋 Preview câu hỏi ({mode_desc}):")
            for i, (q_num, body, q_text) in enumerate(data['unique_blocks'][:5], 1):
                # Hiển thị có dấu "-" hay không
                lines = body.splitlines()
                has_dash = any(line.strip().startswith('-') for line in lines[2:] if line.strip())
                dash_indicator = " 🎯" if has_dash else ""
                print(f"  {i}. Question {q_num}{dash_indicator}: {q_text[:40]}{'...' if len(q_text) > 40 else ''}")
            if len(data['unique_blocks']) > 5:
                print(f"  ... và {len(data['unique_blocks']) - 5} câu khác")
        
        if input("✅ Ghi file? (y/n): ").strip().lower() in ['y', 'yes', '']:
            self.write_output(output, data)
            self.write_log(data, markers)
            print(f"🎉 Xong! File: {output}")

if __name__ == "__main__":
    QuestionFilter().run()
