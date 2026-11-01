from pathlib import Path
import json,html,math,shutil
P=Path(__file__).parent
OLD=P
SCENES=json.loads((OLD/'scenes.json').read_text());PLAN=json.loads((P/'fluent-timing.json').read_text());CAPS=[[q['text'] for q in t['phrases']] for t in PLAN['scenes']]
INK='#263A36'; TEAL='#488B80'; GOLD='#E9AF62'; RED='#AB5546'; GREEN='#C7DAD0'; PAPER='#F6ECD9'
def txt(x,y,t,size=30,color=INK,anchor='middle',cls=''):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}" class="{cls}">{html.escape(str(t))}</text>'
def line(x1,y1,x2,y2,color=INK,w=3,cls='draw'):
 return f'<path d="M{x1} {y1} Q{(x1+x2)/2} {(y1+y2)/2+1.6} {x2} {y2}" fill="none" stroke="{color}" stroke-width="{w}" class="{cls}"/>'
def rect(x,y,w,h,fill=PAPER,r=6,cls=''):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{INK}" stroke-width="2.6" class="{cls}"/>'
def arrow(x1,y1,x2,y2,color=INK,bend=0):
 dx=x2-x1;dy=y2-y1;cx=(x1+x2)/2;cy=(y1+y2)/2+bend;ang=math.atan2(y2-cy,x2-cx);a=12
 pts=f'{x2},{y2} {x2-a*math.cos(ang-.48)},{y2-a*math.sin(ang-.48)} {x2-a*math.cos(ang+.48)},{y2-a*math.sin(ang+.48)}'
 return f'<path d="M{x1} {y1} Q{cx} {cy} {x2} {y2}" fill="none" stroke="{color}" stroke-width="3" class="draw"/><polygon points="{pts}" fill="{color}"/>'
def stage(n,body):return f'<g class="beat beat-{n}">{body}</g>'
def chip(x,y,w,t,fill=GOLD,size=28):return rect(x,y,w,48,fill,5)+txt(x+w/2,y+33,t,size)
def salary(v,caption='triệu / tháng',x=780,y=8,w=310):
 return f'<g class="salary">'+rect(x,y,w,110,'#F7D49C',8)+txt(x+w/2,y+53,v,55)+txt(x+w/2,y+88,caption,25)+'</g>'
def human(x,y,s=1,pose='neutral',shirt=TEAL):
 # One original recurring character. The groups allow an arm to gesture without moving the face.
 arm={'neutral':('M35 95 Q15 117 26 141','M88 96 Q111 113 101 142'),'point':('M35 95 Q15 117 26 141','M88 97 Q117 104 143 75'),'think':('M35 95 Q15 119 26 140','M88 96 Q112 70 88 64'),'work':('M35 95 Q18 122 49 128','M88 96 Q114 117 135 125')}[pose]
 return f'''<g class="human" transform="translate({x} {y}) scale({s})"><ellipse cx="65" cy="214" rx="54" ry="8" fill="#263A3610"/><g class="legs"><path d="M46 150 L44 204 L26 207 M78 150 L83 204 L104 207" fill="none" stroke="{INK}" stroke-width="14" stroke-linecap="round"/></g><path d="M38 85 Q62 78 88 87 L92 156 Q62 167 33 155 Z" fill="{shirt}" stroke="{INK}" stroke-width="3"/><path d="M58 86 L66 114 L74 86" fill="#F6ECD9" stroke="{INK}" stroke-width="2"/><g class="arm"><path d="{arm[0]} {arm[1]}" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/></g><circle cx="64" cy="49" r="35" fill="#F2C89F" stroke="{INK}" stroke-width="3"/><path d="M29 44 Q17 13 48 15 Q63 -4 75 15 Q105 12 100 45 L87 29 L77 37 L62 23 L46 35 L34 34 Z" fill="{INK}"/><path d="M31 46 H59 V62 H33 Z M68 46 H96 V62 H70 Z M59 50 H69" fill="#F6ECD955" stroke="{INK}" stroke-width="3"/><circle cx="46" cy="53" r="3" fill="{INK}"/><circle cx="82" cy="53" r="3" fill="{INK}"/><path d="M52 72 Q64 83 78 70" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/></g>'''
def laptop(x,y,w=180,label='AI'):
 return rect(x,y,w,w*.60,'#E9F1EB',8)+rect(x+10,y+10,w-20,w*.60-20,'#FBF8F0',3)+f'<path d="M{x-12} {y+w*.60} H{x+w+12} L{x+w+22} {y+w*.60+16} H{x-22} Z" fill="{TEAL}" stroke="{INK}" stroke-width="3"/>'+txt(x+w/2,y+w*.36,label,30)
def document(x,y,label='Dự án',fill='#FFF9EF',w=150,h=100):
 return rect(x,y,w,h,fill,3)+''.join(line(x+14,y+k,x+w-14,y+k,w=1.5,cls='') for k in [25,38,51])+txt(x+w/2,y+h-14,label,27)
def bubble(x,y,w,t,fill='#FFF9EF'):
 return rect(x,y,w,64,fill,18)+f'<path d="M{x+30} {y+64} L{x+19} {y+80} L{x+55} {y+64}" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'+txt(x+w/2,y+42,t,30)
def check(x,y):return f'<path d="M{x-14} {y} L{x-2} {y+13} L{x+21} {y-20}" fill="none" stroke="{TEAL}" stroke-width="6" stroke-linecap="round" class="draw"/>'
def cross(x,y):return line(x-16,y-16,x+16,y+16,RED,5)+line(x-16,y+16,x+16,y-16,RED,5)
def building(x,y,w=200,h=210,label='Công ty',fill='#C7DAD0'):
 a=rect(x,y,w,h,fill,2)
 for r in range(3):
  for c in range(3):a+=rect(x+18+c*(w-24)/3,y+22+r*43,29,24,'#FFF9EF',2)
 return a+rect(x+w*.4,y+h-55,w*.2,55,'#E9AF62',2)+txt(x+w/2,y-14,label,32)
def coin(x,y,r=24):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD}" stroke="{INK}" stroke-width="2.5"/>'+txt(x,y+9,'₫',27)
def node(x,y,t,fill=GREEN,w=140):return rect(x-w/2,y-26,w,52,fill,25)+txt(x,y+10,t,29)
def small_model(x,y,label='Mô hình'):
 return rect(x,y,125,100,GREEN,14)+f'<circle cx="{x+42}" cy="{y+38}" r="5" fill="{INK}"/><circle cx="{x+85}" cy="{y+38}" r="5" fill="{INK}"/><path d="M{x+40} {y+63} Q{x+64} {y+77} {x+88} {y+63}" fill="none" stroke="{INK}" stroke-width="3"/>'+txt(x+62,y+133,label,30)
A=[]
# 01: the contradiction is acted out in one workplace.
A.append(''.join([
 stage(1,human(35,135,.92,'think')+document(18,20,'Tốt nghiệp',w=170,h=95)+txt(190,332,'Người mới',30)),
 stage(2,building(800,170,240,178,'Đang tuyển')+salary('45–50',x=779,y=2,w=285)),
 stage(3,arrow(235,220,780,220)+chip(352,157,270,'Cần kinh nghiệm',GREEN)+line(650,187,650,330,RED,6)+txt(650,367,'?',53,RED)),
 stage(4,bubble(265,15,360,'Thiếu người... thiếu ai?', '#FFF9EF')+chip(340,277,300,'Thực tập: có nơi 0đ', '#F2CFBE',29))]))
# 02: seven stepping stones rather than salary cards.
a=stage(1,human(15,136,.82,'point')+txt(85,125,'Bắt đầu',32))
labels=['Sinh viên','Thực tập','Mới nghề','Kinh nghiệm','Cấp cao','Dẫn dắt','Lãnh đạo']
for j,t in enumerate(labels):
 x=235+j*138;y=292-j*30;a+=stage(min(4,1+j//2),node(x,y,t,GREEN if j<5 else '#F7D49C',w=130)+ (arrow(x-115,y+23,x-65,y+3) if j else ''))
a+=stage(4,txt(620,25,'Kỹ năng và trách nhiệm tăng dần',39)+txt(640,350,'Không phải ai cũng đi cùng một tốc độ',31))
A.append(a)
# 03: learning, one block connects into another.
A.append(stage(1,human(80,155,.85,'work')+laptop(245,200,190,'Python')+line(55,300,480,300,w=5)+line(80,300,80,360,w=5)+line(455,300,455,360,w=5))+
 stage(2,document(540,60,'Toán',w=150)+arrow(440,221,570,172))+
 stage(3,document(760,60,'Dữ liệu',w=160)+arrow(696,110,746,110)+txt(730,245,'Xác suất • Đại số',34))+
 stage(4,document(760,260,'Đánh giá',fill=GREEN,w=160)+arrow(840,170,840,246)+bubble(98,20,325,'Hiểu trước, dùng sau')))
# 04: data assembly line.
A.append(stage(1,human(0,142,.82,'work')+salary('0–12',x=810,y=0,w=280)+txt(211,42,'Ảnh đầu vào',32)+document(170,100,'Dữ liệu',w=130)+cross(268,139))+
 stage(2,arrow(316,155,425,155)+document(445,102,'Làm sạch',GREEN,w=150)+check(555,140))+
 stage(3,arrow(610,155,712,155)+document(730,102,'Gán nhãn','#F7D49C',w=150)+txt(808,255,'Đúng nhãn',31))+
 stage(4,arrow(890,155,968,155)+small_model(980,108)+line(170,309,1106,309,w=5)+txt(578,350,'Dữ liệu sai → mô hình học sai',40,RED)))
# 05: a model visibly makes a mistake before a test catches it.
A.append(stage(1,human(16,148,.9,'work')+laptop(210,182,240,'Chatbot')+salary('12–25',x=809,y=0,w=280))+
 stage(2,bubble(230,26,310,'Chính sách đổi trả?')+arrow(488,106,625,155))+
 stage(3,document(635,148,'Trả lời bịa','#F2CFBE',w=210,h=105)+cross(880,203)+txt(755,290,'Không chỉ cần nói hay!',33,RED))+
 stage(4,chip(360,318,420,'Đo lỗi → sửa → thử lại',GREEN,34)+check(988,274)+document(930,162,'Bộ test',GREEN,w=160,h=100)))
# 06: product integration and model training are two different workshops.
A.append(stage(1,human(478,147,.9,'think')+txt(538,82,'Đọc mô tả công việc',40))+
 stage(2,rect(20,25,380,310,'#E3EAE0',13)+txt(210,67,'TÍCH HỢP',43)+laptop(115,105,170,'API')+txt(210,280,'Mô hình có sẵn',31))+
 stage(3,rect(726,25,386,310,'#F4D9B5',13)+txt(919,67,'HUẤN LUYỆN',43)+small_model(857,109,'Dữ liệu riêng')+txt(920,285,'Tự xây mô hình',31))+
 stage(4,arrow(450,170,410,170)+arrow(625,170,714,170)+txt(560,378,'Khác việc, khác kỹ năng, khác cách so lương',30)))
# 07: bridge from classroom to deployment, with people using it.
A.append(stage(1,document(25,166,'Đồ án',w=170,h=120)+human(205,150,.85,'point')+salary('30–60',x=800,y=0,w=290))+
 stage(2,line(380,280,760,280,w=5)+f'<path d="M380 280 Q570 55 760 280" fill="none" stroke="{INK}" stroke-width="4" class="draw"/>'+txt(570,132,'Triển khai',35))+
 stage(3,building(825,185,220,160,'Người dùng thật')+arrow(310,248,372,248)+arrow(765,246,816,246))+
 stage(4,chip(410,302,150,'Dữ liệu',GREEN)+chip(585,302,150,'Chi phí',GOLD)+chip(760,302,150,'Vận hành',GREEN)))
# 08: the hiring filter makes the mismatch visible.
A.append(stage(1,human(20,150,.8,'think')+human(117,174,.68,'neutral',GOLD)+human(198,189,.62,'neutral',RED)+txt(155,110,'Nhiều hồ sơ mới',35))+
 stage(2,f'<path d="M395 70 H745 L625 235 V305 H530 V235 Z" fill="{GREEN}" stroke="{INK}" stroke-width="3"/>'+txt(570,115,'Bộ lọc',37)+arrow(312,183,389,183))+
 stage(3,txt(570,157,'Dự án thật',30)+txt(570,194,'Giao tiếp',30)+txt(572,260,'Tự vận hành',28)+check(736,158))+
 stage(4,building(860,120,230,225,'Vị trí còn trống')+arrow(662,270,852,270)+txt(590,350,'Thiếu ở nhóm này ≠ dễ vào ở nhóm khác',39,RED)))
# 09: senior monitors a system, an alert arrives, then a repair.
A.append(stage(1,human(33,147,.86,'point')+salary('55–80',x=805,y=0,w=285)+laptop(270,180,200,'Hệ thống'))+
 stage(2,laptop(570,44,170,'Chất lượng')+arrow(480,205,560,130)+f'<path d="M590 105 L615 87 L643 92 L674 70 L708 80" fill="none" stroke="{TEAL}" stroke-width="4" class="draw"/>')+
 stage(3,laptop(570,235,170,'Chi phí')+arrow(480,260,560,282)+txt(845,210,'Cảnh báo!',42,RED)+cross(831,252))+
 stage(4,arrow(934,274,776,330,bend=25)+chip(838,315,240,'Theo dõi & sửa',GREEN)+txt(416,80,'Thiết kế cả hệ thống',35)))
# 10: fork road, no ranking between tracks.
A.append(stage(1,human(482,155,.85,'think')+txt(538,113,'Chọn việc muốn làm',38))+
 stage(2,f'<path d="M540 355 Q430 255 215 132" fill="none" stroke="{INK}" stroke-width="4" class="draw"/>'+chip(35,28,285,'DẪN ĐỘI NGŨ',GREEN,37)+human(81,142,.5,'point')+human(174,155,.45)+txt(198,325,'Tuyển • chia việc • giữ người',29))+
 stage(3,f'<path d="M590 355 Q730 255 942 132" fill="none" stroke="{INK}" stroke-width="4" class="draw"/>'+chip(805,28,295,'CHUYÊN GIA',GOLD,37)+laptop(867,140,185,'Bài toán khó')+txt(923,325,'Đào sâu • giải quyết vấn đề',29))+
 stage(4,txt(570,33,'Hai hướng phát triển',35)+txt(573,393,'Không phải hai thứ hạng',37,TEAL)))
# 11: team, priorities and salary belong to the room.
A.append(stage(1,human(10,130,.9,'point')+salary('70–120+',x=796,y=0,w=306))+
 stage(2,rect(350,142,390,155,'#FFF9EF',7)+txt(545,178,'VIỆC CẦN LÀM',37)+chip(378,199,150,'Ưu tiên 1',GOLD,27)+chip(553,199,160,'Ưu tiên 2',GREEN,27))+
 stage(3,human(804,182,.64,'work')+human(920,186,.62,'neutral',GOLD)+human(1030,192,.6,'neutral',RED)+arrow(750,252,800,252))+
 stage(4,txt(500,349,'Quy mô đội + quyền quyết định',39)+bubble(160,4,457,'Trách nhiệm cụ thể là gì?')))
# 12: make the exceptional context dominate, not just the large number.
A.append(stage(1,building(38,170,180,180,'Doanh nghiệp',GREEN)+human(260,187,.7,'think'))+
 stage(2,building(644,87,400,265,'DOANH NGHIỆP RẤT LỚN','#F4D9B5')+building(1003,160,100,192,'','#F4D9B5'))+
 stage(3,salary('390–650',x=667,y=139,w=350)+chip(755,278,257,'NGOẠI LỆ','#F2CFBE',38))+
 stage(4,txt(310,65,'Không phải mức lương phổ biến',36,RED)+arrow(376,200,621,200)+txt(442,165,'Trường hợp hiếm',31)))
# 13: a payslip opens into compensation components.
A.append(stage(1,human(25,143,.85,'think')+document(219,97,'Lương?',w=220,h=200))+
 stage(2,arrow(455,166,540,92)+chip(568,41,230,'Trước thuế?',GREEN,33)+chip(852,41,230,'Sau thuế?',GOLD,33))+
 stage(3,arrow(455,225,540,237)+document(560,199,'Thưởng',w=150)+document(754,199,'Cổ phiếu',w=150)+document(950,199,'Phúc lợi',w=150))+
 stage(4,txt(705,355,'Còn khác năm, nơi làm và loại công ty',39)+txt(332,43,'So cho đúng',36)))
# 14: a small real product travels through an actual pipeline.
A.append(stage(1,human(20,151,.8,'work')+laptop(160,162,165,'Dự án nhỏ'))+
 stage(2,arrow(349,212,415,212)+document(434,165,'Dữ liệu',GREEN,w=150)+txt(510,132,'Nguồn rõ ràng',29))+
 stage(3,arrow(601,212,668,212)+document(690,165,'Đo lỗi',GOLD,w=150)+check(810,202))+
 stage(4,arrow(857,212,923,212)+laptop(940,162,165,'Chạy thật')+txt(615,344,'Cho người khác thử — ghi lại cả giới hạn',40,TEAL)+bubble(94,14,384,'Làm xong một việc nhỏ!')))
# 15: a story ending with a real destination and a still hold.
A.append(stage(1,human(30,155,.86,'point')+node(275,292,'Học',GREEN,140))+
 stage(2,arrow(348,282,459,221)+node(545,208,'Dự án thật',GOLD,180))+
 stage(3,arrow(643,200,754,144)+node(862,125,'Vận hành',GREEN,180))+
 stage(4,arrow(964,121,1033,86)+txt(975,51,'TRÁCH NHIỆM',38)+txt(630,342,'Giá trị tạo ra → thu nhập',53,TEAL)+txt(630,394,'Dự án thật tiếp theo của bạn là gì?',35)))
assert len(A)==15
TOTAL=PLAN['total_duration']
headers=[('LƯƠNG KỸ SƯ AI','Lương cao, sao người mới vẫn khó vào?'),('BẢN ĐỒ NGHỀ','Một hành trình, bảy nấc trách nhiệm'),('01 · SINH VIÊN','Xây nền móng trước khi chạy theo công cụ'),('02 · THỰC TẬP','Việc ít hào nhoáng lại rất quan trọng'),('03 · MỚI VÀO NGHỀ','Làm cho sản phẩm trả lời đúng'),('ĐỌC KỸ CÔNG VIỆC','Cùng tên “AI”, không hẳn cùng việc'),('04 · CÓ KINH NGHIỆM','Bắc cầu từ đồ án đến người dùng thật'),('GIẢI NGHỊCH LÝ','Thiếu người ở đâu? Cạnh tranh ở đâu?'),('05 · KỸ SƯ CẤP CAO','Thiết kế, theo dõi, chịu trách nhiệm'),('NGÃ RẼ NGHỀ NGHIỆP','Quản người hay đào sâu chuyên môn?'),('06 · QUẢN LÝ / CHUYÊN GIA','Đừng chỉ nhìn tên chức danh'),('07 · LÃNH ĐẠO AI','Con số lớn cần đúng bối cảnh'),('ĐỌC SỐ LIỆU','Một khoảng lương chưa nói hết'),('BƯỚC TIẾP THEO','Làm một sản phẩm kiểm chứng được'),('ĐIỀU CẦN NHỚ','Thu nhập đi cùng giá trị tạo ra')]
H=['''<!doctype html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=1280,height=720"><script src="assets/gsap.min.js"></script><style>
@font-face{font-family:'Patrick Hand';src:url('assets/fonts/PatrickHand.ttf')}@font-face{font-family:'Journal Sans';src:url('assets/fonts/JournalSans.ttf')}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1280px;height:720px;overflow:hidden;background:#F6ECD9}#root{width:1280px;height:720px;position:relative;color:#263A36;font-family:'Patrick Hand'}.clip{position:absolute;inset:0}.scene{opacity:0;background:#F6ECD9}#s0{opacity:1}.scene:nth-child(3n+2){background:#EDF0E2}.scene:nth-child(3n+3){background:#F4E3D4}.scene-content{width:100%;height:100%;padding:26px 60px 122px;display:flex;flex-direction:column;gap:8px}.eyebrow{font:22px/1.2 'Journal Sans';letter-spacing:2px;height:28px;color:#466C61}.headline{font-size:54px;line-height:1.14;font-weight:400;height:66px;letter-spacing:.1px}.stage{width:1140px;height:400px;flex-shrink:0;overflow:visible;stroke-linecap:round;stroke-linejoin:round}.stage text{font-family:'Patrick Hand';stroke:none}.source{font:20px/1.3 'Journal Sans';text-align:right;height:27px;color:#405D53}.caption{position:absolute;inset:auto;left:75px;top:580px;width:1130px;min-height:82px;padding:8px 24px;display:flex;align-items:center;justify-content:center;font:29px/1.28 'Journal Sans';text-align:center;color:#263A36;background:#FFF9EF;border:2px solid #263A36;border-radius:12px;opacity:0}.caption mark{background:none;color:#7D382B;font-weight:bold}.corner{display:none;position:absolute;right:32px;bottom:12px;font:19px 'Journal Sans';color:#405D53}.fade{position:absolute;inset:0;background:#182B25;opacity:0;z-index:999}.ground{stroke:#263A36;stroke-width:2;fill:none}
</style></head><body>''',f'<div id="root" data-composition-id="ai-salary-sketch" data-start="0" data-duration="{TOTAL}" data-width="1280" data-height="720" data-fps="24">']
for i,(s,art) in enumerate(zip(SCENES,A)):
 timing=PLAN['scenes'][i];start=timing['start'];dur=timing['duration']+.8 if i<14 else TOTAL-start
 H.append(f'<section id="s{i}" class="clip scene" data-start="{start}" data-duration="{dur}" data-track-index="{i%2}" style="z-index:{i+1}"><div class="scene-content" data-layout-allow-overlap><div class="eyebrow">{headers[i][0]}</div><h1 class="headline">{headers[i][1]}</h1><svg class="stage" viewBox="0 0 1140 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{html.escape(headers[i][1])}" data-layout-allow-overflow><path class="ground" d="M-16 366 Q280 363 570 367 T1158 365" style="opacity:{0 if i==5 else 1}"/>{art}</svg></div><div class="corner" data-layout-allow-overlap>{i+1:02d} / 15</div></section>')
 for j,text in enumerate(CAPS[i]):
  phrase=timing['phrases'][j];st=phrase['start'];caption_duration=phrase['end']-st;escaped=html.escape(text)
  key=next((w for w in ['kinh nghiệm','dữ liệu','trách nhiệm','tham khảo','sản phẩm','AI','dự án','không'] if w in text),None)
  if key:escaped=escaped.replace(key,f'<mark>{key}</mark>',1)
  H.append(f'<div id="c{i}-{j}" class="clip caption" data-start="{st:.6f}" data-duration="{caption_duration:.6f}" data-track-index="3" data-layout-allow-caption-zone style="z-index:200"><span>{escaped}</span></div>')
H.append(f'<audio id="voiceover" src="assets/narration-final.m4a" data-start="0" data-duration="{TOTAL:.6f}" data-track-index="2" data-volume="1"></audio><div id="fade" class="fade" data-layout-ignore></div></div><script>const tl=gsap.timeline({{paused:true}});')
for i in range(15):
 timing=PLAN['scenes'][i];st=timing['start']
 if i>0:H.append(f"tl.fromTo('#s{i}',{{opacity:0}},{{opacity:1,duration:.8,ease:'sine.inOut'}},{st});")
 H.append(f"tl.from('#s{i} .headline',{{y:8,duration:.65,ease:'power3.out'}},{st+.12});") if i==0 else H.append(f"tl.from('#s{i} .headline',{{opacity:0,y:8,duration:.65,ease:'power3.out'}},{st+.12});")
 for j in range(1,5):
  at=max(st+.25,timing['phrases'][j-1]['start']-.5)
  H.append(f"tl.from('#s{i} .beat-{j}',{{opacity:0,y:5,duration:.65,ease:'power2.out'}},{at:.6f});")
  H.append(f"if(document.querySelector('#s{i} .beat-{j} .draw'))tl.from('#s{i} .beat-{j} .draw',{{strokeDasharray:1500,strokeDashoffset:1500,duration:1.05,ease:'sine.inOut'}},{at+.14:.2f});")
 idle=(timing['voice_end']-st-.7)/10
 H.append(f"tl.to('#s{i} .human',{{y:'-=2.5',duration:{idle:.6f},repeat:9,yoyo:true,ease:'sine.inOut'}},{st+.8});")
 if i in {0:2,3:1,4:1,6:1,8:1,10:1,11:3}:
  sat=max(st+.3,timing['phrases'][{0:2,3:1,4:1,6:1,8:1,10:1,11:3}[i]-1]['start']-.45)
  H.append(f"tl.from('#s{i} .salary',{{rotation:-2,scale:.94,transformOrigin:'center',duration:.7,ease:'back.out(1.15)'}},{sat});")
 for j in range(4):
  at=timing['phrases'][j]['start'];end=timing['phrases'][j]['end']
  H.append(f"tl.fromTo('#c{i}-{j}',{{opacity:0}},{{opacity:1,duration:.14,ease:'sine.out'}},{at:.6f});")
  H.append(f"tl.to('#c{i}-{j}',{{opacity:0,duration:.14,ease:'sine.inOut'}},{end-.14:.6f});")
H.append(f"tl.to('#fade',{{opacity:1,duration:.8,ease:'sine.inOut'}},{TOTAL-.8:.6f});window.__timelines={{'ai-salary-sketch':tl}};tl.seek(0);</script></body></html>")
(P/'index.html').write_text('\n'.join(H))
(P/'package.json').write_text(json.dumps({'name':'ai-salary-sketch','private':True,'scripts':{'check':'npx --yes hyperframes@0.8.223 check','render':'npx --yes hyperframes@0.8.223 render','dev':'npx --yes hyperframes@0.8.223 preview'}},indent=2))
# Script, caption summaries and source notes are local editable project inputs.
print(f'Built 15 scenes, 60 speech-aligned beats, {TOTAL:.3f} seconds, 1280x720.')
