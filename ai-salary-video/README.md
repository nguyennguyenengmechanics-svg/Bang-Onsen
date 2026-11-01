# Lương kỹ sư AI — video giải thích

Bản dựng hình 4 phút 34 giây, biên soạn lại từ phụ đề người dùng cung cấp cho https://www.youtube.com/watch?v=9mbIKLKq9UM.

- `script.md`, `narration.txt`: lời dẫn viết mới, không sao chép nguyên văn.
- `source-notes.json`: khoảng lương và đoạn nguồn, cùng giới hạn xác minh.
- `scenes.json`, `captions-short.json`: nội dung đồ hoạ và chữ tóm ý.
- `index.html`, `build.py`: dự án HyperFrames và mã tạo dự án.

Các mức lương chỉ là tham khảo theo phụ đề chưa xác minh độc lập, chưa xác định năm và gross/net. Mức giám đốc 390–650 triệu/tháng là ví dụ ngoại lệ, không phải trung bình hay mức phổ biến. Không đưa phần luật, thuế và thông tin bổ nhiệm chưa kiểm tra vào bản mới.

## Trạng thái âm thanh

Bản dựng hình hiện không có audio. Chữ tóm ý được đặt theo thời gian đọc, không được mô tả là phụ đề đã đồng bộ giọng. Chưa thể đo LUFS hoặc tỷ lệ sound effect/giọng nói khi chưa có giọng đọc.

`edge-tts` đã cài cục bộ, nhưng tên miền dịch vụ tiếng Việt bị mạng từ chối 403. Đề xuất thay đổi được giữ ở `network-request.json`; lưu cấu hình chưa thành công vì draft không cho chỉnh sửa. Sau khi kết nối được áp dụng hoặc có file giọng đọc, cần ghép tiếng, làm phụ đề thực theo âm thanh, đo lại loudness và kiểm tra điểm cắt.

## Xuất lại

Node.js 22+, FFmpeg và Chromium. Không cần worktree mới.

```bash
python3 build.py
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npm run check
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npm run render -- --output Luong-ky-su-AI.mp4 --fps 24 --quality high --workers 4
```

Chồng chữ giữa các scene được đánh dấu có chủ ý chỉ cho crossfade 0,8 giây; trong phần ổn định mỗi cảnh có vùng đọc riêng. Icon chuyển động nhẹ, khung kết dừng hơn 2 giây trước khi mờ.
