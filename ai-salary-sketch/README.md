# Lương kỹ sư AI — bản hoạt hình giải thích

Bản dựng lại theo phong cách video mẫu người dùng cung cấp: 16:9, nền giấy, nhân vật kỹ sư vẽ mới, sơ đồ và đồ vật xuất hiện nối tiếp. Thời lượng 4 phút 34 giây, 1280 × 720, 24 fps.

## Thay đổi so với bản trước

- Thay bố cục thẻ dọc bằng 15 cảnh hoạt hình ngang, 60 diễn biến minh hoạ.
- Một kỹ sư xuyên suốt câu chuyện: học, làm dữ liệu, sửa chatbot, triển khai sản phẩm, vận hành và chọn hướng nghề nghiệp.
- Mỗi cảnh xây dần theo bốn ý, khoảng 4,25 giây một ý. Nhãn gắn trực tiếp với đồ vật, có mũi tên và đường đi.
- Chữ viết tay Patrick Hand có đủ glyph tiếng Việt; chữ tóm ý dùng font sans cục bộ.
- Giữ nguyên kịch bản chủ đề lương AI, không lấy âm thanh hoặc mascot từ mẫu TikTok.

## Trạng thái

**Đây là bản dựng hình chưa có âm thanh.** Chữ tóm ý theo thời gian đọc, chưa phải phụ đề khớp giọng đọc. Dịch vụ đọc tiếng Việt vẫn bị mạng chặn; xem `network-request.json`. Cần có giọng đọc trước khi đồng bộ phụ đề, chọn sound effect nhỏ hơn giọng 10 dB và đo loudness −14 LUFS/đỉnh dưới −1 dBTP. Không có phép đo LUFS cho bản không audio.

Các mức lương giữ đúng phạm vi của phụ đề người dùng cung cấp, chưa được xác minh độc lập, chưa rõ năm và gross/net. Mức 390–650 triệu/tháng được đặt trong bối cảnh ngoại lệ ở doanh nghiệp rất lớn.

## Xem và chỉnh sửa

- `Luong-ky-su-AI-hoat-hinh.mp4`: file xuất.
- `index.html`, `build.py`: nguồn dựng, tự chứa và có thể chỉnh sửa.
- `scenes.json`, `captions-short.json`: dữ liệu lời dẫn và chữ tóm ý.
- `script.md`, `narration.txt`: kịch bản viết lại.
- `REFERENCE.md`, `DESIGN.md`: phân tích mẫu và quy tắc hình ảnh.
- `source-notes.json`: truy nguyên các mức lương.

Node.js 22+, Python 3 và Chromium/FFmpeg. Dùng checkout hiện có; không cần tạo worktree mới.

```bash
python3 build.py
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npm run check
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npm run render -- --output Luong-ky-su-AI-hoat-hinh.mp4 --fps 24 --quality high --workers 4
```

Chuyển cảnh 0,8 giây tạo chồng hình chủ ý, được đánh dấu trong các vùng nội dung. Khung kết dừng khoảng 3 giây rồi mờ 0,8 giây. Phông và GSAP đều nằm trong `assets/`, không cần tải lúc xuất.
