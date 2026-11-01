"""Generate approved Vietnamese narration; model files stay outside the repository."""
import argparse,json,pathlib,wave,re,math
import numpy as np,sherpa_onnx
from content import SCENES
p=pathlib.Path(__file__).resolve().parent
arg=argparse.ArgumentParser();arg.add_argument('--model-dir',required=True);arg.add_argument('--clips-dir',required=True);args=arg.parse_args()
m=pathlib.Path(args.model_dir);out=pathlib.Path(args.clips_dir);out.mkdir(exist_ok=True,parents=True)
cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=str(m/'vi_VN-vais1000-medium.onnx'),tokens=str(m/'tokens.txt'),data_dir=str(m/'espeak-ng-data'),noise_scale=.2,noise_scale_w=.3),num_threads=2))
tts=sherpa_onnx.OfflineTts(cfg)
REPLACE={'3.469':'ba nghìn bốn trăm sáu mươi chín','7.700':'bảy nghìn bảy trăm','1.600':'một nghìn sáu trăm','1.200':'một nghìn hai trăm','2026':'hai nghìn không trăm hai mươi sáu','626':'sáu trăm hai mươi sáu','90%':'chín mươi phần trăm','40%':'bốn mươi phần trăm','80%':'tám mươi phần trăm','25%':'hai mươi lăm phần trăm','75%':'bảy mươi lăm phần trăm','18%':'mười tám phần trăm','15%':'mười lăm phần trăm','3%':'ba phần trăm','20 triệu':'hai mươi triệu','Python':'pai thon','Power BI':'pao ơ bi ai','SQL':'ét kiu eo','JavaScript':'gia va sờ cờ ríp','Java':'gia va','Docker':'đóc cơ','DevOps':'đép óp','Data':'dữ liệu','AI':'trí tuệ nhân tạo','IT':'công nghệ thông tin','TopCV':'tóp xi vi','fresher':'phờ rét sơ','junior':'giu ni ơ','backend':'bách en','remote':'ri mốt','onsite':'on sai','hybrid':'hai bờ rít','JD':'mô tả công việc','QA':'kiểm thử','support':'hỗ trợ kỹ thuật','LLM':'mô hình ngôn ngữ lớn'}
timings=[]
for i,s in enumerate(SCENES):
 row=[]
 for j,txt in enumerate(s['subs']):
  spoken=txt
  for a,b in REPLACE.items():spoken=spoken.replace(a,b)
  audio=tts.generate(spoken,sid=0,speed=1.0)
  assert audio.sample_rate==22050 and len(audio.samples)>0
  f=out/f'{i:02}-{j}.wav'
  with wave.open(str(f),'wb') as w:
   w.setnchannels(1);w.setsampwidth(2);w.setframerate(audio.sample_rate);w.writeframes((np.clip(audio.samples,-1,1)*32767).astype(np.int16).tobytes())
  dur=len(audio.samples)/audio.sample_rate;slot=max(5.0,math.ceil((dur+.6)*10)/10)
  row.append({'caption':txt,'spoken':spoken,'audio_duration':round(dur,4),'duration':slot})
  print(i,j,round(dur,2),slot,flush=True)
 timings.append(row)
(p/'timings.json').write_text(json.dumps(timings,ensure_ascii=False,indent=2)+'\n')
