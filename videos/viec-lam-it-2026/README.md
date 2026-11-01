# Việc làm IT Việt Nam 2026: Người mới còn cơ hội không?

Video hoạt hình tiếng Việt phân tích báo cáo do người dùng cung cấp. Định dạng 1920×1080, 24 fps, dài 3 phút 33 giây; dùng đúng giọng tiếng Việt đã duyệt, nhạc nền nhẹ và phụ đề khớp lời đọc. Không có nhân vật có tên riêng hoặc khẩu hiệu cố định ở chân hình.

- [Video MP4](viec-lam-it-2026.mp4)
- [Kịch bản](kich-ban.txt)
- [Phụ đề](phu-de.srt)
- [Nguồn và giới hạn số liệu](SOURCES.md)
- [Nguồn giọng đọc](assets/AUDIO-CREDITS.md)

Các con số là mô tả mẫu 3.469 tin trong báo cáo, không đại diện mặc định cho toàn thị trường hoặc cả năm. Nêu rõ giới hạn thời điểm, nguồn TopCV, phạm vi mức lương và mẫu số các nhóm.

## Dựng lại từ các tài sản âm thanh đã lưu

```sh
cd videos/viec-lam-it-2026
python3 generate.py
npm run check
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npx --yes hyperframes@0.8.226 render --fps 24 --workers 4 --output viec-lam-it-2026.mp4
```

Để tạo lại giọng đọc: cài sherpa-onnx==1.12.32 và numpy, tải mô hình theo AUDIO-CREDITS.md, xác minh SHA-256 rồi giải nén ngoài checkout. Chạy synthesize.py --model-dir <thư-mục-mô-hình> --clips-dir <thư-mục-WAV>, rồi mix_audio.py --clips-dir <thư-mục-WAV> và generate.py. Không đưa mô hình hoặc môi trường Python vào Git.
