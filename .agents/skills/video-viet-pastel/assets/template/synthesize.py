"""Generate approved Vietnamese narration; model files stay outside the repository."""
import argparse,json,pathlib,wave,re,math
import numpy as np,sherpa_onnx
from content import SCENES
p=pathlib.Path(__file__).resolve().parent
arg=argparse.ArgumentParser();arg.add_argument('--model-dir',required=True);arg.add_argument('--clips-dir',required=True);args=arg.parse_args()
m=pathlib.Path(args.model_dir);out=pathlib.Path(args.clips_dir);out.mkdir(exist_ok=True,parents=True)
cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=str(m/'vi_VN-vais1000-medium.onnx'),tokens=str(m/'tokens.txt'),data_dir=str(m/'espeak-ng-data'),noise_scale=.2,noise_scale_w=.3),num_threads=2))
tts=sherpa_onnx.OfflineTts(cfg)
REPLACE={'AI':'trí tuệ nhân tạo','IT':'công nghệ thông tin','Python':'pai thon','SQL':'ét kiu eo','Docker':'đóc cơ'}
timings=[]
for i,s in enumerate(SCENES):
 row=[]
 for j,txt in enumerate(s['subs']):
  spoken=s.get('spoken',s['subs'])[j]
  if 'spoken' not in s:
   for a,b in REPLACE.items():spoken=re.sub(r'(?<!\w)'+re.escape(a)+r'(?!\w)',b,spoken)
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
