# Lộ trình sự nghiệp kỹ sư AI

Video hoạt hình tiếng Việt, 1920×1080, 24 fps, dài 3 phút.
Nội dung mô tả một kỹ sư AI nói chung, không dùng nhân vật có tên riêng.

- [Video có âm thanh](lo-trinh-ky-su-ai.mp4)
- [Kịch bản](kich-ban.txt)
- [Phụ đề](phu-de.srt)

## Âm thanh
Giọng đọc tổng hợp tiếng Việt đọc từng câu phụ đề, bắt đầu sau 0,12 giây trong mỗi khoảng 5 giây. Nhạc nền nhỏ được tổng hợp mới. Dùng đúng mô hình và thiết lập của mẫu “Viet-ro-hon” được người dùng duyệt: speaker 0, speed 1.0, noise_scale 0.2, noise_scale_w 0.3. Không tăng tốc lời đọc; mỗi câu nằm trọn trong khoảng phụ đề tương ứng.

Giọng đọc dùng sherpa-onnx và mô hình Piper vi_VN-vais1000-medium (speaker 0). Model card ghi giấy phép CC BY 4.0; xem [thông tin nguồn âm thanh](assets/AUDIO-CREDITS.md) và [model card](assets/VOICE-MODEL-CARD.txt).

## Chạy lại
Cần Node.js 22+, FFmpeg và Chromium.

```sh
cd videos/lo-trinh-ky-su-ai
python3 generate.py
npm run check
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npx --yes hyperframes@0.8.226 render --fps 24 --workers 4 --output lo-trinh-ky-su-ai.mp4
```

`index.html`: hoạt hình và hai track âm thanh đã lưu cục bộ.
`generate.py`: tạo lại hoạt hình, kịch bản, phụ đề.
`DESIGN.md`: hướng mỹ thuật.

Đã bỏ hai dòng chữ cố định ở chân hình; giữ tiêu đề, thẻ kỹ năng và phụ đề nội dung.
