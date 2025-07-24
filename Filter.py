# Lọc đáp án trong file với tùy chọn file input

import re
import os
import json
import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Set

class QuestionFilter:
    def __init__(self):
        self.default_input_file = "Input.txt"
        self.input_file = ""  # Sẽ được set trong get_input_file()
        self.log_file = "Log.txt"
        self.config_file = "config.json"
        self.backup_dir = "backups"
        
    def list_available_files(self) -> List[str]:
        """Liệt kê các file có thể dùng làm input"""
        supported_extensions = ['.txt', '.docx', '.doc']
        available_files = []
        
        try:
            for file in os.listdir('.'):
                if any(file.lower().endswith(ext) for ext in supported_extensions):
                    if os.path.isfile(file):
                        available_files.append(file)
        except Exception as e:
            print(f"⚠️ Lỗi khi liệt kê file: {e}")
            
        return sorted(available_files)
    
    def get_input_file(self) -> str:
        """Cho phép user chọn hoặc nhập file input"""
        print("📁 Chọn file input:")
        print("=" * 30)
        
        available_files = self.list_available_files()
        
        if available_files:
            print("📂 Các file có sẵn:")
            for i, file in enumerate(available_files, 1):
                size = os.path.getsize(file)
                size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
                print(f"  ▫️  {i}. {file} ({size_str})")
            print(f"  ▫️  {len(available_files) + 1}. Nhập tên file khác")
            print(f"  ▫️  {len(available_files) + 2}. Tạo file '{self.default_input_file}' mẫu")
            
            while True:
                try:
                    choice = input(f"\nChọn (1-{len(available_files) + 2}): ").strip()
                    
                    if not choice:
                        print("❌ Vui lòng nhập lựa chọn!")
                        continue
                        
                    choice_num = int(choice)
                    
                    if 1 <= choice_num <= len(available_files):
                        selected_file = available_files[choice_num - 1]
                        print(f"✅ Đã chọn: {selected_file}")
                        return selected_file
                    elif choice_num == len(available_files) + 1:
                        return self.get_custom_input_filename()
                    elif choice_num == len(available_files) + 2:
                        self.create_sample_input()
                        return ""  # Exit để user thêm nội dung
                    else:
                        print(f"❌ Chọn từ 1 đến {len(available_files) + 2}!")
                        
                except ValueError:
                    print("❌ Vui lòng nhập số!")
                except KeyboardInterrupt:
                    print("\n👋 Thoát chương trình!")
                    exit(0)
        else:
            print("📂 Không tìm thấy file nào!")
            print("1. Nhập tên file")
            print(f"2. Tạo file '{self.default_input_file}' mẫu")
            
            while True:
                try:
                    choice = input("Chọn (1/2): ").strip()
                    if choice == '1':
                        return self.get_custom_input_filename()
                    elif choice == '2':
                        self.create_sample_input()
                        return ""
                    else:
                        print("❌ Chọn 1 hoặc 2!")
                except KeyboardInterrupt:
                    print("\n👋 Thoát chương trình!")
                    exit(0)
    
    def get_custom_input_filename(self) -> str:
        """Nhập tên file input tùy chỉnh"""
        while True:
            filename = input("📝 Nhập tên file input (có đuôi .txt): \n➡️  ").strip()
            
            if not filename:
                print("❌ Vui lòng nhập tên file!")
                continue
                
            # Tự động thêm .txt nếu không có đuôi
            if '.' not in filename:
                filename += '.txt'
                print(f"🔧 Tự động thêm đuôi: {filename}")
            
            # Kiểm tra file có tồn tại không
            if not os.path.exists(filename):
                print(f"❌ File '{filename}' không tồn tại!")
                choice = input("1. Nhập lại | 2. Tạo file mới | 3. Thoát (1/2/3): ").strip()
                
                if choice == '2':
                    try:
                        # Tạo file mới với nội dung mẫu
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write("📝 Ghi nội dung câu hỏi dưới đây:\n\n")
                            f.write("Question 1\n0.3 / 0.3 pts\nVí dụ: Bạn thấy như thế nào?\n  Tuyệt.\n  Tuyệt2.\n")
                        print(f"✅ Đã tạo file '{filename}'. Thêm nội dung câu hỏi vào đó rồi chạy lại.")
                        return ""
                    except Exception as e:
                        print(f"❌ Lỗi tạo file: {e}")
                        continue
                elif choice == '3':
                    print("👋 Thoát chương trình!")
                    exit(0)
                # choice == '1' thì tiếp tục vòng lặp
                continue
            
            # Kiểm tra quyền đọc file
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content_preview = f.read(100)  # Đọc 100 ký tự đầu
                print(f"✅ File hợp lệ. Preview: {content_preview[:50]}...")
                return filename
            except Exception as e:
                print(f"❌ Không thể đọc file '{filename}': {e}")
                choice = input("1. Nhập lại | 2. Thoát (1/2): ").strip()
                if choice == '2':
                    print("👋 Thoát chương trình!")
                    exit(0)
                continue
        
    def create_sample_input(self) -> None:
        """Tạo file input mẫu"""
        try:
            with open(self.default_input_file, "w", encoding="utf-8") as f:
                f.write("📝 Ghi nội dung câu hỏi dưới đây:\n\n")
                f.write("Question 1\n0.3 / 0.3 pts\nVí dụ: Bạn thấy như thế nào?\n  Tuyệt.\n  Tuyệt2.\n\n")
                f.write("Question 2\n0.5 / 0.5 pts\nCâu hỏi thứ hai:\n  Đáp án A\n  Đáp án B\n  Đáp án C\n\n")
                f.write("Question 3\nIncorrect\n0 / 0.5 pts\nCâu sai (sẽ bị loại):\n  Sai A\n  Sai B\n")
            print(f"✅ Đã tạo file '{self.default_input_file}' với nội dung mẫu.")
            print("📝 Thêm nội dung câu hỏi của bạn vào file này rồi chạy lại chương trình.")
        except Exception as e:
            print(f"❌ Lỗi tạo file mẫu: {e}")
            
    def backup_file(self, filename: str) -> str:
        """Backup file trước khi xử lý"""
        try:
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{self.backup_dir}/{Path(filename).stem}_{timestamp}{Path(filename).suffix}"
            
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as src, \
                     open(backup_name, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
                return backup_name
        except Exception as e:
            print(f"⚠️ Không thể backup: {e}")
        return ""

    def load_config(self) -> Dict:
        """Load cấu hình từ file JSON"""
        default_config = {
            "invalid_markers": ["Incorrect", "0 /", "0.0 /"],
            "output_formats": [".txt", ".docx", ".json", ".csv"],
            "auto_backup": True,
            "last_input_file": ""
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return {**default_config, **json.load(f)}
        except Exception as e:
            print(f"⚠️ Lỗi đọc config, dùng mặc định: {e}")
        
        return default_config

    def save_config(self, config: Dict) -> None:
        """Lưu cấu hình"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Không thể lưu config: {e}")

    def read_input_file(self, filename: str) -> str:
        """Đọc file input với xử lý lỗi"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
            return content
        except FileNotFoundError:
            print(f"❌ Không tìm thấy file '{filename}'")
            return ""
        except UnicodeDecodeError:
            print(f"❌ Lỗi encoding file '{filename}'. Thử UTF-8 hoặc CP1252")
            try:
                with open(filename, "r", encoding="cp1252") as f:
                    return f.read().strip()
            except:
                return ""
        except Exception as e:
            print(f"❌ Lỗi đọc file: {e}")
            return ""

    def fix_content_format(self, content: str) -> str:
        """Sửa định dạng nội dung"""
        # Fix các lỗi định dạng phổ biến
        fixes = [
            (r"(?<!\n)(Question \d+)", r"\n\1"),
            (r"(Incorrect)(Question \d+)", r"\1\n\2"),
            (r"(\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?\s*pts)([^\n])", r"\1\n\2"),
            (r"\n\s*\n\s*\n", r"\n\n")  # Loại bỏ dòng trống thừa
        ]
        
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)
        
        return content

    def validate_content(self, content: str) -> Tuple[bool, List[str]]:
        """Validate định dạng nội dung"""
        errors = []
        
        if not content:
            errors.append("File rỗng")
            return False, errors
            
        if not re.search(r"\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?\s*pts", content):
            errors.append("Không tìm thấy định dạng điểm '... pts'")
            
        question_count = len(re.findall(r"Question \d+", content))
        if question_count == 0:
            errors.append("Không tìm thấy câu hỏi nào với format 'Question X'")
            
        return len(errors) == 0, errors

    def get_output_filename(self, config: Dict) -> str:
        """Lấy tên file output với validation"""
        print("\n📝 Nhập tên file output:")
        print("Các định dạng hỗ trợ:", ", ".join(config["output_formats"]))
        
        while True:
            filename = input("Tên file + đuôi (vd: 'chuong1.txt'): ").strip()
            
            if not filename:
                print("❌ Vui lòng nhập tên file!")
                continue
                
            if '.' not in filename:
                print(f"⚠️ Không có đuôi file! Hỗ trợ: {', '.join(config['output_formats'])}")
                choice = input("1. Nhập lại | 2. Thoát (1/2): ").strip()
                if choice == '2':
                    print("👋 Thoát chương trình!")
                    exit(0)
                continue
                
            file_ext = Path(filename).suffix.lower()
            if file_ext not in config["output_formats"]:
                print(f"⚠️ Định dạng '{file_ext}' chưa hỗ trợ!")
                print(f"Hỗ trợ: {', '.join(config['output_formats'])}")
                continue
                
            return filename

    def get_invalid_markers(self, config: Dict) -> List[str]:
        """Lấy danh sách từ khóa đánh dấu sai"""
        print(f"\n🔴 Từ khóa đánh dấu câu sai hiện tại: {config['invalid_markers']}")
        choice = input("Sử dụng mặc định? (y/n): ").strip().lower()
        
        if choice in ['n', 'no']:
            markers = input("Nhập từ khóa (cách nhau bởi dấu phẩy): ").strip()
            if markers:
                return [m.strip() for m in markers.split(',')]
        
        return config['invalid_markers']

    def normalize_question_for_comparison(self, question_text: str) -> str:
        """
        Chuẩn hóa câu hỏi để so sánh, bỏ qua dấu "-" đứng đầu
        """
        # Loại bỏ khoảng trắng và xuống dòng thừa
        normalized = question_text.strip()
        
        # Nếu câu hỏi bắt đầu bằng dấu "-", loại bỏ dấu "-" và khoảng trắng sau nó
        if normalized.startswith('-'):
            # Tìm và loại bỏ dấu "-" đầu tiên cùng với khoảng trắng theo sau
            normalized = re.sub(r'^-\s*', '', normalized)
        
        return normalized.strip()

    def parse_questions(self, content: str) -> List[Tuple[str, str]]:
        """Parse câu hỏi từ content"""
        # Regex pattern
        pattern = r"(Question\s+(\d+)\n\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?\s*pts\n([\s\S]+?))(?=Question\s+\d+\n\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?\s*pts\n|\Z)"
        matches = re.findall(pattern, content, re.IGNORECASE)
        
        questions = []
        for full_block, question_number, after_pts in matches:
            questions.append((question_number, after_pts.strip()))
            
        return questions

    def filter_questions(self, questions: List[Tuple[str, str]], invalid_markers: List[str]) -> Dict:
        """Lọc câu hỏi với xử lý dấu '-'"""
        seen_questions: Set[str] = set()  # Lưu trữ câu hỏi đã chuẩn hóa để so sánh
        unique_blocks: List[Tuple[str, str, str]] = []  # Thêm original_question để lưu câu gốc
        removed_blocks = 0
        incorrect_questions: Set[str] = set()
        format_errors: List[str] = []
        duplicate_info: List[str] = []  # Thông tin về câu trùng lặp
        
        for question_number, content_after_pts in questions:
            lines = content_after_pts.strip().splitlines()
            question_text_only = lines[0].strip() if lines else ""
            
            # Kiểm tra câu sai
            is_incorrect = any(marker in content_after_pts for marker in invalid_markers)
            if is_incorrect:
                incorrect_questions.add(f"Câu hỏi {int(question_number):02}")
                continue
            
            # Kiểm tra định dạng đáp án
            if len(lines) < 2 or not re.search(r"\s{1,}[\w\-–•\d]", lines[1]):
                format_errors.append(f"⚠️ Câu {question_number}: không có phương án trả lời")
            
            # Chuẩn hóa câu hỏi để so sánh (bỏ dấu "-" nếu có)
            normalized_question = self.normalize_question_for_comparison(question_text_only)
            
            # Lọc trùng lặp dựa trên nội dung đã chuẩn hóa
            if normalized_question not in seen_questions:
                seen_questions.add(normalized_question)
                unique_blocks.append((question_number, content_after_pts, question_text_only))
            else:
                removed_blocks += 1
                # Ghi nhận thông tin trùng lặp
                duplicate_info.append(f"Câu {question_number}: '{question_text_only[:50]}...' (trùng với câu đã có)")
        
        return {
            'unique_blocks': unique_blocks,
            'removed_blocks': removed_blocks,
            'incorrect_questions': incorrect_questions,
            'format_errors': format_errors,
            'total_questions': len(questions),
            'duplicate_info': duplicate_info
        }

    def write_output(self, filename: str, data: Dict) -> None:
        """Ghi file output theo định dạng"""
        file_ext = Path(filename).suffix.lower()
        
        try:
            if file_ext == '.json':
                self._write_json(filename, data)
            elif file_ext == '.csv':
                self._write_csv(filename, data)
            else:  # .txt, .docx
                self._write_text(filename, data)
                
            print(f"✅ Đã ghi vào file '{filename}'")
        except Exception as e:
            print(f"❌ Lỗi ghi file: {e}")

    def _write_text(self, filename: str, data: Dict) -> None:
        """Ghi file text - đánh số lại câu hỏi theo thứ tự tăng dần"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write("✅ Đã lọc câu hỏi trùng lặp\n")
            f.write(f"📊 Thống kê: {len(data['unique_blocks'])}/{data['total_questions']} câu hỏi\n")
            f.write(f"📁 File input: {self.input_file}\n\n")
            
            for i, (q_num, content, original_question) in enumerate(data['unique_blocks'], 1):
                f.write(f"Câu hỏi {i}:\n{content}\n\n")

    def _write_json(self, filename: str, data: Dict) -> None:
        """Ghi file JSON"""
        output_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'input_file': self.input_file,
            'statistics': {
                'total': data['total_questions'],
                'unique': len(data['unique_blocks']),
                'removed': data['removed_blocks'],
                'incorrect': len(data['incorrect_questions'])
            },
            'questions': [
                {'id': q_num, 'content': content, 'original_question': original_question}
                for q_num, content, original_question in data['unique_blocks']
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

    def _write_csv(self, filename: str, data: Dict) -> None:
        """Ghi file CSV - đánh số lại câu hỏi theo thứ tự tăng dần"""
        import csv
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['New_Question_ID', 'Original_Question_ID', 'Content', 'Original_Question'])
            for i, (q_num, content, original_question) in enumerate(data['unique_blocks'], 1):
                writer.writerow([str(i), q_num, content.replace('\n', ' | '), original_question])

    def write_log(self, data: Dict, invalid_markers: List[str]) -> None:
        """Ghi file log với thông tin chi tiết về trùng lặp"""
        try:
            with open(self.log_file, "w", encoding="utf-8") as log:
                log.write(f"📊 Báo cáo xử lý - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                log.write("=" * 50 + "\n\n")
                
                log.write(f"📁 File input: {self.input_file}\n\n")
                
                log.write("📈 Thống kê:\n")
                log.write(f"    ▫️ Tổng câu hỏi: {data['total_questions']}\n")
                log.write(f"    ▫️ Câu trùng lặp: {data['removed_blocks']}\n")
                log.write(f"    ▫️ Câu sai: {len(data['incorrect_questions'])}\n")
                log.write(f"    ▫️ Câu hợp lệ: {len(data['unique_blocks'])}\n\n")
                
                if data['incorrect_questions']:
                    log.write(f"❌ Câu sai (từ khóa: {invalid_markers}):\n")
                    for q in sorted(data['incorrect_questions']):
                        log.write(f"    ▫️ {q}\n")
                    log.write("\n")
                
                if data['duplicate_info']:
                    log.write("🔄 Chi tiết câu trùng lặp (đã bỏ qua dấu '-' khi so sánh):\n")
                    for info in data['duplicate_info']:
                        log.write(f"    ▫️ {info}\n")
                    log.write("\n")
                
                if data['format_errors']:
                    log.write("⚠️ Cảnh báo định dạng:\n")
                    for error in data['format_errors']:
                        log.write(f"    ▫️ {error}\n")
                    log.write("\n")
                
                if not data['incorrect_questions'] and not data['format_errors'] and not data['duplicate_info']:
                    log.write("✅ Không có lỗi định dạng hoặc trùng lặp\n")
                    
        except Exception as e:
            print(f"⚠️ Không thể ghi log: {e}")

    def run(self) -> None:
        """Chạy chương trình chính"""
        print("🔍 Bộ lọc câu hỏi - Phiên bản nâng cao")
        print("=" * 50)
        
        # Load config
        config = self.load_config()
        
        # Chọn file input
        self.input_file = self.get_input_file()
        if not self.input_file:  # User chọn tạo file mẫu
            return
        
        # Lưu file input vào config
        config['last_input_file'] = self.input_file
        self.save_config(config)
        
        # Backup nếu cần
        if config.get("auto_backup", True):
            backup_file = self.backup_file(self.input_file)
            if backup_file:
                print(f"📦 Đã backup: {backup_file}")
        
        # Đọc và validate nội dung
        content = self.read_input_file(self.input_file)
        if not content:
            return
            
        is_valid, errors = self.validate_content(content)
        if not is_valid:
            print("\n❌ Lỗi định dạng file:")
            for error in errors:
                print(f"    ▫️ {error}")
            return
        
        # Sửa định dạng
        content = self.fix_content_format(content)
        
        # Lấy thông tin từ user
        output_filename = self.get_output_filename(config)
        invalid_markers = self.get_invalid_markers(config)
        
        # Xử lý câu hỏi
        print("\n⏳ Đang xử lý...")
        questions = self.parse_questions(content)
        if not questions:
            print("❌ Không tìm thấy câu hỏi nào!")
            return
            
        result_data = self.filter_questions(questions, invalid_markers)
        
        # Preview kết quả
        print(f"\n📊 Preview:")
        print(f"    ▫️ File input: {self.input_file}")
        print(f"    ▫️ Tổng: {result_data['total_questions']} câu")
        print(f"    ▫️ Hợp lệ: {len(result_data['unique_blocks'])} câu")
        print(f"    ▫️ Loại bỏ: {result_data['removed_blocks'] + len(result_data['incorrect_questions'])} câu")
        if result_data['duplicate_info']:
            print(f"    ▫️ Lưu ý: Đã bỏ qua dấu '-' khi so sánh trùng lặp")
        
        confirm = input("\n✅ Tiếp tục ghi file? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes', '']:
            print("❌ Đã hủy!")
            return
        
        # Ghi file output và log
        self.write_output(output_filename, result_data)
        self.write_log(result_data, invalid_markers)
        
        print(f"\n🎉 Hoàn thành!")
        print(f"📄 Kết quả: '{output_filename}'")
        print(f"📋 Log: '{self.log_file}'")

# Chạy chương trình
if __name__ == "__main__":
    filter_app = QuestionFilter()
    filter_app.run()
