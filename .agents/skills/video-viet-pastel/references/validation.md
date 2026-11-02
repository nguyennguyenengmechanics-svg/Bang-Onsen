# Xác minh gói kỹ năng

Đã kiểm tra tại lúc đóng gói:

- YAML frontmatter của SKILL.md hợp lệ, các liên kết nội bộ trỏ tới file có thật, toàn bộ Python parse được.
- Tạo một dự án mới từ template; thử lại cùng đích bị từ chối, không ghi đè file.
- Helper mô hình xác minh SHA-256 của archive đã tải và giải nén an toàn vào thư mục cache mới; không cần bỏ xác minh TLS hay checksum.
- Chạy thực tế pipeline mới: 2 cảnh, 6 câu, giọng đã duyệt, hai track MP3, phụ đề và HTML. Không tăng tốc lời đọc.
- HyperFrames check hoàn thành thành công; đã xem một khung hình của MP4 đã xuất.
- MP4 thử nghiệm dài 30 giây, 1920×1080, H.264 và AAC. File thử ở ngoài repository, không đưa vào gói kỹ năng.
- ZIP mở được, có SKILL.md tại gốc thư mục kỹ năng, không chứa model ONNX, venv hay cache.

Đây là bằng chứng về gói và môi trường đã kiểm tra, không bảo đảm mọi máy mới đã có các dependency. Mỗi video mới vẫn cần chạy kiểm tra riêng.
