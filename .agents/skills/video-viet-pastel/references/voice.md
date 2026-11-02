# Giọng tiếng Việt đã được duyệt

Người dùng chọn mẫu **Viet-ro-hon.mp3**, được đóng gói ở `../assets/voice-approved.mp3` tính từ thư mục tham chiếu này. Giọng C và các giọng cũ **không phải** giọng được chọn cuối cùng.

| Thiết lập | Giá trị |
| --- | --- |
| Engine | sherpa-onnx 1.12.32 |
| Model | Piper vi_VN-vais1000-medium |
| Speaker ID | 0 |
| Speed | 1.0 |
| noise_scale | 0.2 |
| noise_scale_w | 0.3 |
| Sample rate gốc | 22050 Hz |
| Ngữ điệu | Gần gũi, bình thản, rõ tiếng Việt, không diễn hoặc lên xuống quá mức |

Nguồn tải mô hình:
`https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-vi_VN-vais1000-medium.tar.bz2`

SHA-256 archive:
`fa1367710767d36ed5cf13b4a449e20c35ffd12791c2e47c2e64142bfa55551a`

Dùng `scripts/fetch_voice.py <thư-mục-cache>` để tải, kiểm tra checksum và giải nén. Model và venv lưu ngoài checkout dự án; script không đổi chính sách mạng hay bỏ TLS. Nếu mạng chặn, báo đúng bước bị chặn, không tự đổi sang giọng thấp chất lượng hơn.

Model card ghi **CC BY 4.0**. Giữ model card và ghi nguồn engine, model, dataset URL theo `assets/template/assets/VOICE-MODEL-CARD.txt`. Không nhầm với giấy phép CC BY-NC-SA của model vivos-x_low cũ.

## Phát âm và nhịp

- Khớp nội dung lời đọc với phụ đề. Cho phép diễn đạt cách đọc số, chữ viết tắt và thuật ngữ bằng trường `spoken`; không thay nội dung phân tích.
- Viết rõ số tiền, phần trăm, năm, đơn vị và khoảng giá trị trong `spoken`. Tránh để bộ đọc đoán ký hiệu.
- Ngắt câu theo ý, chèn nghỉ ngắn tự nhiên; không làm giọng quá điệu.
- Thời lượng mỗi câu mặc định `max(5 giây, thời lượng lời đọc + 0,6 giây)`, onset khoảng 0,15 giây. Câu dài nên biên tập ngắn hoặc cho thời gian dài hơn; không dùng atempo để tăng tốc giọng đã duyệt.
- Nhạc nền gốc được tổng hợp nhẹ, không dùng lại nhạc không rõ quyền từ video tham khảo.
- Nếu thay model, speaker hoặc dịch vụ làm đổi chất giọng, gửi mẫu để người dùng duyệt trước khi thay vào video hoàn chỉnh.
