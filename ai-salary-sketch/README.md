# Lương kỹ sư AI — hoạt hình có lồng tiếng Việt

4 phút 34 giây, 1280 × 720, 24 fps. Nhân vật kỹ sư vẽ mới, sơ đồ và đồ vật xuất hiện theo từng ý, tham khảo phong cách video mẫu người dùng gửi.

## Bản cập nhật

- Đã lồng tiếng Việt bằng eSpeak NG chạy cục bộ: giọng máy cơ bản, không phải giọng neural và không mô phỏng người dẫn của mẫu.
- 60 cụm giọng đọc, ghép theo thời gian chữ xuất hiện; số và thuật ngữ được chuẩn hoá để phát âm rõ hơn.
- Đã bỏ toàn bộ hai loại chú thích nguồn nhỏ ở cuối khung hình theo yêu cầu người dùng.
- Thông tin nguồn và giới hạn xác minh vẫn được lưu trong tài liệu dự án.

## Nội dung dự án

- `renders/Luong-ky-su-AI-hoat-hinh.mp4`: bản MP4 có tiếng trên GitHub.
- `assets/narration-final.m4a`: giọng đọc đã cân âm lượng.
- `spoken-narration.txt`, `voice-plan.json`: lời đọc thực tế và thời điểm đo từ số mẫu WAV.
- `phu-de-vi.srt`: phụ đề tiếng Việt theo các cụm đọc.
- `index.html`, `build.py`, `scenes.json`, `captions-short.json`: nguồn đồ hoạ và chữ.
- `script.md`, `narration.txt`: kịch bản tham khảo đầy đủ; bản đọc thực tế dùng các câu tóm ý trong `spoken-narration.txt`.
- `REFERENCE.md`, `DESIGN.md`, `source-notes.json`: tham chiếu phong cách, quy tắc hình và xuất xứ các mức lương.
- `voice-loudness.json`, `verification.json`: bằng chứng kiểm tra âm thanh và bản xuất.

## Chỉnh sửa và xuất lại

Node.js 22+, Python 3, FFmpeg và Chrome/Chromium. Dùng checkout hiện có, không cần tạo worktree mới. Media, GSAP và font đều được lưu cục bộ.

```bash
python3 build.py
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npm run check
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npm run render -- --output Luong-ky-su-AI-long-tieng.mp4 --fps 24 --quality high --workers 4
```

Nếu cần tạo lại giọng đọc, cài bộ đọc một lần rồi chạy các script; không cần kết nối dịch vụ đọc tiếng Việt trực tuyến:

```bash
python3 -m pip install --target voice-tools espeakng-loader==0.2.4
python3 produce_voice.py
python3 master_voice.py
```

`master_voice.py` đo và cân lại trên AAC thực tế. Khi thay đổi câu chữ phải kiểm tra lại thời lượng cụm, đồng bộ hình và đo lại MP4 sau mã hoá. Bộ công cụ và WAV trung gian không được đóng gói trong repository.

Các mức lương chỉ là tham khảo theo phụ đề người dùng cung cấp, chưa được xác minh độc lập, chưa rõ năm và gross/net. Mức 390–650 triệu/tháng là trường hợp ngoại lệ tại doanh nghiệp rất lớn. Bản mới không đưa phần luật và thuế chưa xác minh vào nội dung.
