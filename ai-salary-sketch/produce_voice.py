from pathlib import Path
import json,re,subprocess,wave
from synthesize_local import synth,sr
P=Path(__file__).parent;out=P/'assets/voice';out.mkdir(exist_ok=True)
caps=json.loads((P/'captions-short.json').read_text())
replacements={'45–50':'bốn mươi lăm đến năm mươi','0–12':'không đến mười hai','12–25':'mười hai đến hai mươi lăm','0–2':'không đến hai','2–4':'hai đến bốn','30–60':'ba mươi đến sáu mươi','55–80':'năm mươi lăm đến tám mươi','70–120':'bảy mươi đến một trăm hai mươi','390–650':'ba trăm chín mươi đến sáu trăm năm mươi','/tháng':' mỗi tháng','0đ':'không đồng','→':', rồi ','≠':' không đồng nghĩa với ','AI':'ây ai','Python':'pai thờn','Chatbot':'Chát bót','chatbot':'chát bót'}
plan=[];total=274;mix=bytearray(int(total*48000)*2)
for i,groups in enumerate(caps):
 for j,text in enumerate(groups):
  spoken=text
  for a,b in replacements.items():spoken=spoken.replace(a,b)
  spoken=re.sub(r'\s+',' ',spoken).strip()
  raw=out/f'raw-{i:02}-{j}.wav';processed=out/f'phrase-{i:02}-{j}.wav';dur=synth(spoken,raw,rate=160)
  # Compress only phrases longer than their available caption window, preserving pitch.
  speed=max(1,dur/3.25)
  fx=f'atempo={speed:.6f},highpass=f=85,lowpass=f=7600,afade=t=in:d=0.012,afade=t=out:st={max(0,min(dur,3.25)-.035):.4f}:d=0.035'
  subprocess.run(['ffmpeg','-v','error','-i',str(raw),'-af',fx,'-ar','48000','-ac','1','-c:a','pcm_s16le',str(processed),'-y'],check=True)
  with wave.open(str(processed),'rb') as w:pcm=w.readframes(w.getnframes());dd=w.getnframes()/w.getframerate()
  start=i*18+.85+j*4.25+.08;offset=int(start*48000)*2;mix[offset:offset+len(pcm)]=pcm
  plan.append({'scene':i+1,'phrase':j+1,'caption':text,'spoken':spoken,'start':start,'end':start+dd,'raw_duration':dur,'speed':speed,'duration':dd})
with wave.open(str(P/'assets/narration-local.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(mix)
(P/'voice-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');(P/'spoken-narration.txt').write_text('\n\n'.join(x['spoken'] for x in plan)+'\n')
print('Vietnamese phrases:',len(plan),'active speech seconds:',round(sum(x['duration'] for x in plan),2),'max speed adjustment:',round(max(x['speed'] for x in plan),3))
assert len(plan)==60 and all(x['end']<=((x['scene']-1)*18+.85+(x['phrase']-1)*4.25+3.45) for x in plan)
