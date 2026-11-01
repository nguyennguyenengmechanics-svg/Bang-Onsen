# Lộ trình sự nghiệp kỹ sư AI

Bản dựng hoạt hình tiếng Việt, 1920×1080, 24 fps, 144 giây.
Tham khảo ngôn ngữ hình ảnh của video do người dùng cung cấp; nhân vật và hình vẽ được dựng mới.

## Hiện trạng
- Có hoạt hình, kịch bản, phụ đề và chuyển cảnh.
- Chưa có giọng thuyết minh. Dịch vụ TTS tiếng Việt tại translate.google.com trả về HTTP 403 do chính sách mạng. Yêu cầu tên miền đã được lưu vào bản nháp cài đặt môi trường, chưa xác minh quyền truy cập sau khi áp dụng.
- Phụ đề hiện theo thời gian đọc của bản dựng, cần căn lại theo âm thanh thật khi có thuyết minh.
- Không dùng các con số lương chưa kiểm chứng trong tài liệu thành lời hứa thu nhập.

## Chạy lại
Node.js 22+, FFmpeg và Chromium.

```sh
cd videos/lo-trinh-ky-su-ai
npm run check
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npx --yes hyperframes@0.8.226 render --fps 24 --workers 4 --output lo-trinh-ky-su-ai-ban-dung-hinh.mp4
```

`index.html`: hoạt hình có thể chỉnh sửa.
`kich-ban.txt`: nội dung thuyết minh.
`phu-de.srt`: phụ đề bản dựng.
`DESIGN.md`: bảng màu và hướng mỹ thuật.
