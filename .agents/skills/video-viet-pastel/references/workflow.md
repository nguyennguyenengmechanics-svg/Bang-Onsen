# Chạy kỹ năng trong một môi trường mới

## Vị trí và công cụ

Các đường dẫn mẫu dưới đây dùng repository hiện tại, không phụ thuộc `/workspace/ai-career` của phiên làm việc cũ.

Cần Python 3.12+, Node.js 22+, FFmpeg, Chromium/Chrome. Dùng công cụ có sẵn trước; giữ xác minh TLS, chữ ký và checksum. Nếu kết nối bị chặn, dùng cấu hình mạng được hỗ trợ, không lách proxy.

```sh
python3 .agents/skills/video-viet-pastel/scripts/new_project.py videos/chu-de-moi
python3 -m venv /workspace/video-runtime/venv
/workspace/video-runtime/venv/bin/pip install sherpa-onnx==1.12.32 numpy
python3 .agents/skills/video-viet-pastel/scripts/fetch_voice.py /workspace/video-runtime/models
```

`/workspace/video-runtime` là ví dụ thư mục có thể ghi ngoài checkout; chọn đường dẫn phù hợp môi trường thực tế. Không ghi vào thư mục hệ thống hoặc yêu cầu sudo khi không cần.

## Dữ liệu cảnh

Sửa `content.py` trong dự án mới. `SCENES` là danh sách dict:

- `kicker`: nhãn ngắn; `title`: một ý chính.
- `kind`: `hero`, `cards`, `flow`, `bars`, `ranks`, `split`.
- `items`: `[(giá_trị, nhãn), ...]`; riêng `bars` là `[(nhãn, chuỗi_giá_trị, độ_dài_0_đến_1), ...]`.
- `note`: chú thích cần thiết, có thể để chuỗi rỗng. Không tự thêm slogan hoặc dòng về nhân vật.
- `subs`: các câu phụ đề ngắn.
- `spoken`: tùy chọn, danh sách cùng độ dài với `subs`, chứa cách đọc tiếng Việt đã chuẩn hóa số và thuật ngữ. Không được thêm/bớt ý so với phụ đề. Nếu không có, script chỉ thay một số thuật ngữ thông dụng; vẫn phải rà cách đọc số theo chủ đề.

Không sao chép số liệu từ dự án cũ. Biểu đồ dùng tỷ lệ chính xác hoặc mốc giới hạn có nhãn rõ; nếu thiếu giá trị, dùng thẻ hoặc thứ hạng.

Mẫu bố cục đã kiểm tra cho 2–3 thẻ và 2–4 dòng biểu đồ. Nếu nội dung dài hơn, chia cảnh hoặc điều chỉnh bố cục và kiểm tra lại, đừng làm nhỏ chữ đến khó đọc. Mẫu cấp track riêng cho phụ đề và âm thanh, hỗ trợ dưới 100 cảnh; video dài hơn phải kiểm tra lại track và lớp.

## Tạo âm thanh, phụ đề và HTML

Sau khi sửa nội dung:

```sh
cd videos/chu-de-moi
/workspace/video-runtime/venv/bin/python synthesize.py \
  --model-dir /workspace/video-runtime/models/vits-piper-vi_VN-vais1000-medium \
  --clips-dir /workspace/video-runtime/clips/chu-de-moi
/workspace/video-runtime/venv/bin/python mix_audio.py \
  --clips-dir /workspace/video-runtime/clips/chu-de-moi
python3 generate.py
npx --yes hyperframes@0.8.226 check
npx --yes hyperframes@0.8.226 snapshot --at 5,15,25
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npx --yes hyperframes@0.8.226 render \
  --fps 24 --quality standard --workers 4 --output chu-de-moi.mp4
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,sample_rate -of json chu-de-moi.mp4
```

Đường dẫn Chrome là ví dụ: tìm executable thực tế. Chọn số workers theo tài nguyên. Nếu npm package đã cache và mạng hạn chế, có thể dùng `npx --offline hyperframes ...`.

Synthesize tạo WAV và `timings.json` từ thời lượng thật. Mix giữ tốc độ giọng gốc, tạo hai track MP3 có nguồn/giấy phép. Generate tạo `index.html`, `kich-ban.txt`, `phu-de.srt`. Thay nội dung thì chạy lại toàn bộ chuỗi; không để âm thanh cũ đọc phụ đề mới.

## Bàn giao và kiểm tra

- Đọc báo cáo check; sửa lỗi, rà cảnh báo. Xem các snapshot bằng công cụ xem ảnh, gồm hero frame, cảnh số liệu dày, chuyển cảnh và cuối video.
- Kiểm tra MP4 thực tế có cả video và âm thanh, mọi câu nằm trọn trong slot, âm lượng không clipping; không coi một stream AAC rỗng là thuyết minh.
- Ghi `README.md`, `SOURCES.md` nếu có dữ liệu, và nguồn âm thanh; copy một hero frame làm `anh-xem-truoc.png`.
- Không thay giấy phép giọng đã duyệt bằng model cũ. Không upload model, WAV trung gian, venv, cache hoặc nguồn tài liệu riêng tư chưa được phép.
- Trả link MP4 tải/xem được. Nếu cần Studio handoff, dùng `hyperframes preview --background` và xác minh `--status`; chỉ chia sẻ địa chỉ có thể truy cập trong giao diện thực tế.

## Cài ở repository khác

Copy toàn bộ thư mục `video-viet-pastel` vào `.agents/skills/` của repository mới. Thêm vào `AGENTS.md` của repository mới quy tắc: khi người dùng yêu cầu tạo video theo phong cách đã duyệt, đọc `.agents/skills/video-viet-pastel/SKILL.md`. Giữ chỉ dẫn có sẵn và không tự ghi đè chúng. Sau khi hệ thống nhận lại kỹ năng, có thể gọi bằng `$video-viet-pastel`.

Đây là kỹ năng theo tệp và repository, không phải plugin đã đăng ký toàn tài khoản. Trong cuộc trò chuyện mới không gắn repository hoặc chưa cài kỹ năng, cung cấp lại gói ZIP hoặc link SKILL.md.
