# Lương kỹ sư AI — giọng Việt neural đọc liền đoạn

Video khoảng 4 phút 47 giây, 1280 × 720, 24 fps. Dùng giọng VAIS1000/Piper VITS neural đúng đoạn mẫu người dùng đã nghe và đồng ý.

## Những gì đã sửa

- Thay giọng tổng hợp cơ bản bằng mô hình giọng Việt neural, giữ đúng giọng và tốc độ của mẫu được duyệt.
- Viết lại lời dẫn cho các câu nối ý tự nhiên. Số tiền được chuyển thành chữ đầy đủ trước khi tổng hợp tiếng.
- Tổng hợp 15 đoạn liên tục; bỏ cách xếp câu vào các ô thời gian cố định và khoảng lặng dài giữa từng câu.
- Căn 60 cụm phụ đề bằng đặc trưng âm thanh MFCC/DTW, rồi cho minh hoạ xuất hiện theo từng ý. Không có hai cụm phụ đề đè nhau, không vắt câu qua chỗ cắt.
- Giữ việc xoá các dòng chú thích nguồn ở cuối khung hình theo yêu cầu trước đó.

## Tệp chính

- `renders/Luong-ky-su-AI-hoat-hinh.mp4`: video cập nhật trên GitHub.
- `assets/narration-final.m4a`: âm thanh neural đã cân âm lượng.
- `script.md`, `fluent-script.json`, `spoken-narration.txt`: lời dẫn mới và lời đọc đã chuẩn hoá.
- `fluent-timing.json`, `voice-plan.json`, `phu-de-vi.srt`: dữ liệu thời gian căn theo âm thanh.
- `index.html`, `build.py`: nguồn đồ hoạ.
- `voice-loudness.json`, `final-mp4-loudness.json`, `verification.json`: số đo và kết quả kiểm tra.

## Xuất lại

Cần Node.js 22+, Python 3, FFmpeg, Chromium. Dùng checkout hiện có, không cần worktree mới. Giọng đọc và font được lưu trong dự án, nên xuất lại video không cần tải mô hình.

```bash
python3 build.py
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npm run check
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npm run render -- --output Luong-ky-su-AI-giong-neural.mp4 --fps 24 --quality high --workers 4
```

Nếu cần sửa lời dẫn và tạo lại giọng trên Linux:

```bash
python3 -m pip install --target neural-runtime -r requirements-neural.txt
python3 setup_neural_model.py
python3 generate_fluent_voice.py
python3 master_voice.py
python3 build.py
```

Chỉnh lời ở `fluent-script.json`. Không sửa riêng thời gian phụ đề rồi giữ nguyên âm thanh cũ. Sau mỗi bản mới cần đo lại LUFS/true peak trên MP4 cuối và kiểm tra đồng bộ. Cảnh báo `line_unread` của bộ kiểm tra dùng cách đếm từ có thể đánh dấu các câu phụ đề tiếng Việt; thời gian thực tế được căn theo lời đọc, mỗi cụm hơn 3 giây.

## Nguồn bộ giọng

Mô hình [Piper Vietnamese VAIS1000 medium](https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models), chạy bằng sherpa-onnx 1.13.3. Dataset [VAIS-1000 Vietnamese Speech Synthesis Corpus](https://ieee-dataport.org/documents/vais-1000-vietnamese-speech-synthesis-corpus), giấy phép CC BY 4.0 theo model card; xem `VOICE_MODEL_CARD.md`. Các checksum trong script ghim đúng artifact đã dùng để tạo đoạn mẫu người dùng duyệt. Trọng số mô hình và bộ chạy không được đóng gói trong repository.

Nguồn mức lương vẫn được lưu ở `source-notes.json`; các khoảng lương chưa xác minh độc lập và không phải cam kết thu nhập. Mức giám đốc là ví dụ ngoại lệ, không phải mức phổ biến. Video không sao chép giọng hoặc âm thanh người dẫn TikTok mẫu.
