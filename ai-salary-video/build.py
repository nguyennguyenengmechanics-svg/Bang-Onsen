from pathlib import Path
import json, html
p=Path(__file__).parent
# Original narration and graphics, based on the user-supplied source, not copied dialogue.
scenes=[
('01 · CÂU HỎI','Lương cao.\nSao vẫn khó vào?','45–50','triệu đồng / tháng','Một ví dụ tuyển dụng trong nguồn','briefcase',[
'Một tin tuyển kỹ sư AI đưa ra mức lương bốn mươi lăm đến năm mươi triệu mỗi tháng.',
'Nhưng ở đầu bên kia, có sinh viên thực tập chưa được nhận phụ cấp.',
'Hai câu chuyện ấy không nhất thiết mâu thuẫn với nhau.',
'Điều khác biệt nằm ở kinh nghiệm và trách nhiệm mà mỗi công việc đòi hỏi.']),
('02 · BẢN ĐỒ NGHỀ','Bảy nấc nghề,\nkhác kỳ vọng','HỌC → LÀM','→ DẪN DẮT','Chức danh không phải lịch thăng tiến cố định','ladder',[
'Hãy nhìn nghề này qua bảy nấc, bắt đầu từ sinh viên và thực tập sinh.',
'Tiếp theo là người mới, kỹ sư có kinh nghiệm, rồi kỹ sư cấp cao.',
'Sau đó, con đường tách sang quản lý hoặc chuyên gia trước khi tới lãnh đạo.',
'Đây là khung giải thích, không phải lịch thăng tiến áp dụng cho mọi người.']),
('03 · SINH VIÊN','Học nền móng\ntrước công cụ','TOÁN + CODE','DỮ LIỆU + ĐÁNH GIÁ','AI không chỉ là viết câu lệnh cho chatbot','book',[
'Ở giai đoạn đi học, ưu tiên nền tảng toán, lập trình và cách đánh giá kết quả.',
'Đại số tuyến tính, xác suất và Python giúp bạn hiểu điều gì đang diễn ra.',
'Công cụ có thể thay đổi, còn cách kiểm tra một mô hình vẫn rất quan trọng.',
'Học ngành công nghệ thông tin rồi chuyển sang AI cũng là một hướng đi.']),
('04 · THỰC TẬP','Dữ liệu sạch\nđứng trước mô hình','0–12','triệu đồng / tháng','Các ví dụ phụ cấp trong phụ đề nguồn','data',[
'Khung không đến mười hai triệu ở đây là những ví dụ từ các nơi tuyển khác nhau.',
'Không thể dùng nó để khẳng định mọi thực tập sinh đều nhận từng ấy tiền.',
'Công việc ban đầu có thể là thu thập ảnh, làm sạch dữ liệu và gán nhãn.',
'Điều đáng hỏi thêm là bạn có được tham gia một dự án thật hay không.']),
('05 · MỚI VÀO NGHỀ','Bằng cấp là đầu.\nSản phẩm là tiếp.','12–25','triệu đồng / tháng','Nguồn mô tả nhóm kinh nghiệm 0–2 năm','code',[
'Với người mới đi làm, phụ đề nêu khung tham khảo mười hai đến hai mươi lăm triệu.',
'Bạn cần nền tảng học máy và ít nhất một dự án có thể giải thích rõ.',
'Chẳng hạn, một chatbot phải trả lời đúng chính sách thay vì chỉ nói trôi chảy.',
'Đo lỗi, sửa dữ liệu và kiểm tra lại thường chiếm nhiều thời gian hơn bạn nghĩ.']),
('06 · ĐỌC KỸ MÔ TẢ','Cùng tên AI,\nkhác việc làm','TÍCH HỢP','≠ HUẤN LUYỆN','Đọc công việc trước khi so lương','branch',[
'Một vị trí dùng mô hình có sẵn để xây sản phẩm cho khách hàng.',
'Vị trí khác tập trung huấn luyện mô hình bằng dữ liệu và hạ tầng riêng.',
'Hai hướng đều cần chuyên môn, nhưng bộ kỹ năng và đầu việc không giống nhau.',
'Vì vậy, đừng so hai mức lương chỉ dựa vào cùng một chữ AI trong chức danh.']),
('07 · CÓ KINH NGHIỆM','Khoảng cách là\nchạy được thật','30–60','triệu đồng / tháng','Nguồn mô tả nhóm kinh nghiệm 2–4 năm','gear',[
'Ở nhóm hai đến bốn năm kinh nghiệm, nguồn nêu khoảng ba mươi đến sáu mươi triệu.',
'Điểm khác biệt là khả năng đưa giải pháp vào sử dụng, rồi giữ nó hoạt động ổn định.',
'Bạn còn phải hiểu dữ liệu, chi phí, lỗi hệ thống và yêu cầu của khách hàng.',
'Số năm đi làm chỉ có ý nghĩa khi đi cùng những việc bạn thực sự đã làm.']),
('08 · GIẢI NGHỊCH LÝ','Thiếu người giỏi\n≠ dễ tuyển mới','DỰ ÁN THẬT','+ GIAO TIẾP + VẬN HÀNH','Thiếu ở một nhóm, cạnh tranh ở nhóm khác','bridge',[
'Doanh nghiệp có thể thiếu người nhiều kinh nghiệm trong khi nhận rất nhiều hồ sơ mới.',
'Một bên cần người tự xử lý vấn đề, còn bên kia vẫn cần được hướng dẫn.',
'Tiếng Anh và khả năng phối hợp với khách hàng cũng có thể là điều kiện tuyển dụng.',
'Khoảng cách ấy giải thích vì sao lương cao không đồng nghĩa ai mới ra trường cũng dễ vào.']),
('09 · KỸ SƯ CẤP CAO','Thiết kế hệ thống.\nGánh kết quả.','55–80','triệu đồng / tháng','Khung tham khảo cấp cao trong phụ đề','system',[
'Với kỹ sư cấp cao, nguồn đưa ra khoảng năm mươi lăm đến tám mươi triệu mỗi tháng.',
'Công việc mở rộng từ một tính năng sang kiến trúc, triển khai và giám sát cả hệ thống.',
'Bạn phải biết khi nào kết quả kém đi, tại sao chi phí tăng và cần sửa ở đâu.',
'Mức lương cao hơn đi cùng phạm vi quyết định và hậu quả lớn hơn khi quyết định sai.']),
('10 · NGÃ RẼ','Dẫn đội ngũ\nhay đào sâu?','QUẢN LÝ','HOẶC CHUYÊN GIA','Hai hướng phát triển, không phải hai thứ hạng','branch',[
'Sau nhiều năm, bạn có thể chọn dẫn dắt đội ngũ hoặc đào sâu một mảng kỹ thuật.',
'Quản lý dành nhiều thời gian cho tuyển dụng, phân công và xử lý các ưu tiên.',
'Chuyên gia tập trung giải quyết bài toán khó và xây tiêu chuẩn cho cả nhóm.',
'Không có lựa chọn tốt cho tất cả, hãy nhìn vào loại công việc bạn muốn làm lâu dài.']),
('11 · QUẢN LÝ AI','Lương đổi theo\nphạm vi trách nhiệm','70–120+','triệu đồng / tháng','Khung quản lý được nhắc trong nguồn','team',[
'Nguồn nhắc mức quản lý AI từ bảy mươi đến một trăm hai mươi triệu trở lên.',
'Nhưng trưởng nhóm, chuyên gia chính và quản lý một mảng không tự động cùng mức lương.',
'Quy mô đội ngũ, doanh nghiệp và phạm vi quyết định đều làm con số thay đổi.',
'Khi so lời mời làm việc, hãy hỏi rõ trách nhiệm thay vì chỉ nhìn tên chức danh.']),
('12 · LÃNH ĐẠO AI','Con số lớn,\ntrường hợp hiếm','390–650','triệu đồng / tháng','NGOẠI LỆ · doanh nghiệp rất lớn','crown',[
'Con số ba trăm chín mươi đến sáu trăm năm mươi triệu là trường hợp đặc biệt trong nguồn.',
'Đó không phải mức lương phổ biến cho mọi người mang chức danh giám đốc AI.',
'Vai trò này quyết định chiến lược, ngân sách và cách cả tổ chức sử dụng công nghệ.',
'Không nên lấy mức đãi ngộ ngoại lệ làm kỳ vọng mặc định khi bắt đầu học nghề.']),
('13 · ĐỌC SỐ CHO ĐÚNG','Một khoảng lương\nchưa nói hết','GROSS / NET?','THƯỞNG / CỔ PHIẾU?','Khác năm, địa điểm, vai trò → khó so trực tiếp','check',[
'Trước khi so sánh, cần biết con số là trước hay sau thuế và có gồm thưởng không.',
'Địa điểm làm việc, loại công ty và thời điểm khảo sát cũng ảnh hưởng rất nhiều.',
'Các khoảng trong video lấy từ phụ đề bạn cung cấp, chưa được kiểm chứng độc lập.',
'Vì vậy, hãy xem chúng là điểm bắt đầu để tìm hiểu, không phải lời hứa thu nhập.']),
('14 · BƯỚC TIẾP THEO','Làm một dự án\ncó thể kiểm chứng','DỮ LIỆU THẬT','KẾT QUẢ ĐO ĐƯỢC','Nêu bài toán, cách làm, lỗi và giới hạn','rocket',[
'Nếu đang học, hãy chọn một bài toán nhỏ và làm nó đủ hoàn chỉnh để người khác thử.',
'Ghi rõ dữ liệu đến từ đâu, đánh giá thế nào và hệ thống còn mắc những lỗi gì.',
'Khi đi thực tập, hỏi người hướng dẫn và hỏi sản phẩm cuối cùng mình sẽ đóng góp.',
'Một hồ sơ kể được câu chuyện ấy sẽ rõ ràng hơn một danh sách dài tên công cụ.']),
('15 · ĐIỀU CẦN NHỚ','Thu nhập đi cùng\ngiá trị tạo ra','BẠN ĐANG Ở','NẤC NÀO?','Đặt mục tiêu kỹ năng trước mục tiêu chức danh','heart',[
'Con đường AI có nhiều cơ hội, nhưng các mức lương cao không xuất hiện ngay từ cửa vào.',
'Bạn cần thời gian tích luỹ nền tảng, dự án và khả năng chịu trách nhiệm.',
'Hãy chọn nấc tiếp theo bằng điều mình cần học và vấn đề mình muốn giải quyết.',
'Bạn đang ở đâu trên hành trình ấy, và dự án thật tiếp theo của bạn là gì?'])]
D=18;total=len(scenes)*D+4
(p/'scenes.json').write_text(json.dumps([dict(zip(['kicker','title','value','unit','note','icon','narration'],s)) for s in scenes],ensure_ascii=False,indent=2)+'\n')
(p/'narration.txt').write_text('\n\n'.join(' '.join(s[-1]) for s in scenes)+'\n')
(p/'script.md').write_text('# Lương kỹ sư AI — kịch bản mới\n\nNguồn tham khảo: phụ đề người dùng cung cấp cho https://www.youtube.com/watch?v=9mbIKLKq9UM. Chưa xác minh độc lập; năm nguồn chưa rõ. Không sử dụng âm thanh hoặc hình ảnh của kênh gốc.\n\n'+ '\n\n'.join(f'## {i*D:03d}–{(i+1)*D:03d}s · {s[0]}\n\n'+ ' '.join(s[-1]) for i,s in enumerate(scenes)))
icons={
'briefcase':'<rect x="20" y="35" width="120" height="90" rx="12"/><path d="M55 35 V20 H105 V35 M20 65 Q80 90 140 65 M68 72 H92"/>',
'book':'<path d="M80 38 Q46 18 15 35 V125 Q48 108 80 128 Q112 108 145 125 V35 Q114 18 80 38 Z M80 38 V128"/>',
'data':'<ellipse cx="80" cy="30" rx="52" ry="18"/><path d="M28 30 V118 C28 143 132 143 132 118 V30 M28 60 C28 85 132 85 132 60 M28 88 C28 113 132 113 132 88"/>',
'code':'<path d="M55 40 L15 80 L55 120 M105 40 L145 80 L105 120 M92 23 L68 137"/>',
'branch':'<path d="M80 140 V85 M80 85 L30 40 M80 85 L130 40 M15 60 V25 H50 M110 25 H145 V60"/>',
'ladder':'<path d="M30 135 V25 M125 135 V25 M30 45 H125 M30 75 H125 M30 105 H125 M30 135 H125"/>',
'gear':'<circle cx="80" cy="80" r="45"/><circle cx="80" cy="80" r="19"/><path d="M80 12 V32 M80 128 V148 M12 80 H32 M128 80 H148 M30 30 L45 45 M115 115 L130 130 M30 130 L45 115 M115 45 L130 30"/>',
'bridge':'<path d="M15 125 V55 M145 125 V55 M15 55 Q80 155 145 55 M15 100 H145 M40 82 V100 M65 92 V100 M95 92 V100 M120 82 V100"/>',
'system':'<rect x="50" y="15" width="60" height="45" rx="7"/><rect x="5" y="103" width="60" height="45" rx="7"/><rect x="95" y="103" width="60" height="45" rx="7"/><path d="M80 60 V82 M35 103 V82 H125 V103"/>',
'check':'<path d="M34 19 H126 V143 H34 Z M52 52 L61 61 L78 42 M88 53 H111 M52 91 L61 100 L78 81 M88 92 H111"/>',
'crown':'<path d="M23 48 L51 75 L80 25 L109 75 L137 48 L122 126 H38 Z M38 139 H122"/>',
'rocket':'<path d="M58 105 C36 75 75 20 130 20 C130 75 75 115 58 105 Z M60 75 L23 83 L28 115 L58 105 M85 105 L77 142 L45 137 L58 105 M35 124 L18 141"/><circle cx="97" cy="53" r="13"/>',
'heart':'<path d="M80 135 L28 83 C-4 43 46 10 80 49 C114 10 164 43 132 83 Z"/>',
 'team':'<circle cx="80" cy="43" r="22"/><circle cx="27" cy="60" r="16"/><circle cx="133" cy="60" r="16"/><path d="M44 130 V106 C44 71 116 71 116 106 V130 M4 130 V105 C4 87 25 80 40 90 M120 90 C135 80 156 87 156 105 V130"/>'}
# Salary bar excludes the exceptional director case; it never shares a misleading common axis.
H=['''<!doctype html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=720,height=1280"><script src="assets/gsap.min.js"></script><style>
@font-face{font-family:'Journal Sans';src:url('assets/fonts/JournalSans.ttf')}@font-face{font-family:'Journal Serif';src:url('assets/fonts/JournalSerif.ttf')}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:720px;height:1280px;overflow:hidden;background:#F7F2E7;color:#144E49;font-family:'Journal Sans'}#root{width:720px;height:1280px;position:relative}.clip{position:absolute;inset:0}.scene{background:#F7F2E7}.scene-content{width:100%;height:100%;padding:50px 50px 180px;display:flex;flex-direction:column;gap:22px}.kicker{font-size:23px;letter-spacing:2px;line-height:1.4}.line{height:3px;background:#43877B;width:100%;flex-shrink:0}.headline{font:400 53px/1.22 'Journal Serif';height:142px;max-width:620px;white-space:pre-line;letter-spacing:-1.8px}.visual{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;width:100%;height:370px;flex-shrink:0;border:2px solid #43877B;border-radius:28px;background:#F0EBDD}.icon{width:150px;height:150px;stroke:#43877B;stroke-width:5;fill:none;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}.value{font-size:69px;line-height:1.2;letter-spacing:-2px;text-align:center;white-space:nowrap;font-weight:bold}.unit{font-size:25px;line-height:1.3;text-align:center}.note{font-size:26px;line-height:1.45;text-align:center;max-width:620px;min-height:80px}.source-label{font-size:19px;line-height:1.5;text-align:center;color:#326D65;max-width:620px}.caption{position:absolute;inset:auto;opacity:0;left:50px;top:980px;width:620px;min-height:170px;display:flex;align-items:center;justify-content:center;text-align:center;padding:18px 23px;border-radius:18px;background:#144E49;color:#F7F2E7;font-size:30px;line-height:1.43}.caption mark{background:none;color:#EBC77B;font-weight:bold}.progress{position:absolute;left:50px;bottom:75px;width:620px;height:4px;background:#43877B}.page{position:absolute;bottom:32px;left:50px;width:620px;display:flex;justify-content:space-between;font-size:19px;letter-spacing:1px}.fade{position:absolute;inset:0;background:#101E1B;opacity:0;z-index:1000}
</style></head><body>''',f'<div id="root" data-composition-id="ai-salary" data-start="0" data-duration="{total}" data-width="720" data-height="1280" data-fps="30">']
for i,s in enumerate(scenes):
 kicker,title,value,unit,note,icon,narr=s;start=i*D;dur=D+.8 if i<len(scenes)-1 else D+4
 H+=[f'<section id="s{i}" class="clip scene" data-start="{start}" data-duration="{dur}" data-track-index="{i%2}" style="z-index:{i+1}"><div class="scene-content" data-layout-allow-overlap><div class="kicker">{kicker}</div><div class="line" data-layout-ignore></div><h1 class="headline">{title}</h1><div class="visual"><svg class="icon" viewBox="0 0 160 160">{icons[icon]}</svg><div class="value">{html.escape(value)}</div><div class="unit">{unit}</div></div><div class="note">{note}</div><div class="source-label">Lương từ phụ đề nguồn · chưa xác minh độc lập · chưa rõ gross/net.</div></div><div class="progress" data-layout-ignore></div><div class="page" data-layout-allow-overlap><span>LƯƠNG KỸ SƯ AI</span><span>{i+1:02d} / {len(scenes):02d}</span></div></section>']
 # Planned caption timing is a reading guide, not claimed to be synchronized to an unavailable voice track.
 for j,text in enumerate(json.loads((p/"captions-short.json").read_text())[i]):
  st=start+.85+j*4.25;du=4.25
  key=next((w for w in ['kinh nghiệm','dữ liệu','trách nhiệm','tham khảo','sản phẩm','AI','khác nhau','kiểm tra','dự án','không'] if w in text),None)
  escaped=html.escape(text)
  if key:escaped=escaped.replace(key,'<mark>'+key+'</mark>',1)
  H+=[f'<div id="c{i}-{j}" class="clip caption" data-start="{st:.2f}" data-duration="{du}" data-track-index="3" data-layout-allow-caption-zone style="z-index:200"><span>{escaped}</span></div>']
H+=['<div id="fade" class="fade" data-layout-ignore></div></div><script>const tl=gsap.timeline({paused:true});']
for i,s in enumerate(scenes):
 st=i*D
 H += [f"tl.from('#s{i}',{{opacity:0,duration:.8,ease:'sine.inOut'}},{st});",f"tl.from('#s{i} .headline',{{y:15,opacity:0,duration:.7,ease:'power3.out'}},{st+.1});",f"tl.from('#s{i} .icon',{{scale:.91,opacity:0,duration:.8,ease:'power2.out'}},{st+.25});",f"tl.from('#s{i} .value',{{y:8,opacity:0,duration:.65,ease:'power1.out'}},{st+.4});",f"tl.to('#s{i} .icon',{{y:-5,duration:1.8,repeat:9,yoyo:true,ease:'sine.inOut'}},{st+.8});",f"tl.fromTo('#s{i} .progress',{{scaleX:0,transformOrigin:'left'}},{{scaleX:1,duration:{D},ease:'none'}},{st});"]
 for j in range(4):
  cs=st+.85+j*4.25
  H += [f"tl.fromTo('#c{i}-{j}',{{opacity:0}},{{opacity:1,duration:.22,ease:'sine.out'}},{cs:.2f});",f"tl.to('#c{i}-{j}',{{opacity:0,duration:.8,ease:'sine.inOut'}},{cs+3.45:.2f});"]
# Final picture and headline stop moving at 225s, hold 3 seconds, then fade.
H += [f"tl.to('#fade',{{opacity:1,duration:.8,ease:'sine.inOut'}},{total-.8});", "window.__timelines={'ai-salary':tl};tl.seek(0);</script></body></html>"]
(p/'index.html').write_text('\n'.join(H));(p/'package.json').write_text(json.dumps({'name':'ai-salary-explainer','private':True,'scripts':{'check':'npx --yes hyperframes@0.8.223 check','render':'npx --yes hyperframes@0.8.223 render','dev':'npx --yes hyperframes@0.8.223 preview'}},indent=2))
print('Duration',total,'seconds; narration words',len((p/'narration.txt').read_text().split()))
