from pathlib import Path
import subprocess,re,json
P=Path(__file__).parent;src=P/'assets/narration-neural.wav'
def measure(f):
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-af','loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 return json.loads(re.findall(r'\{[\s\S]*?\}',r.stderr)[-1])
# Speech synthesis has sharp peaks. Compress before gain and leave AAC reconstruction headroom.
base=P/'assets/narration-compressed.wav'
subprocess.run(['ffmpeg','-v','error','-i',str(src),'-af','acompressor=threshold=0.18:ratio=2:attack=8:release=120:makeup=1','-ar','48000','-c:a','pcm_s24le',str(base),'-y'],check=True)
initial=measure(base);gain=-14-float(initial['input_i']);history=[];target=P/'assets/narration-final.m4a'
for i in range(10):
 fx=f'volume={gain}dB,alimiter=limit=0.77:attack=5:release=50:level=false:latency=true'
 subprocess.run(['ffmpeg','-v','error','-i',str(base),'-af',fx,'-c:a','aac','-b:a','192k',str(target),'-y'],check=True)
 m=measure(target);history.append({'gain_db':gain,'measurement':m});print('AAC measured',m['input_i'],'LUFS;',m['input_tp'],'dBTP',flush=True)
 error=-14-float(m['input_i'])
 if abs(error)<=.08 and float(m['input_tp'])< -1:break
 gain+=error
(P/'voice-loudness.json').write_text(json.dumps({'initial':initial,'aac_calibration':history},indent=2)+'\n')
assert abs(float(m['input_i'])+14)<=.1 and float(m['input_tp'])< -1
