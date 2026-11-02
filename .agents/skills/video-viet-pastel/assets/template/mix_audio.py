import argparse,json,pathlib,wave,subprocess,math
import numpy as np
p=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--clips-dir',required=True);args=parser.parse_args();clips=pathlib.Path(args.clips_dir)
timings=json.loads((p/'timings.json').read_text());rate=22050;total=sum(t['duration'] for row in timings for t in row);voice=np.zeros(round(rate*total),dtype=np.float32);cursor=0
for i,row in enumerate(timings):
 for j,t in enumerate(row):
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(clips/f'{i:02}-{j}.wav'),'-af','loudnorm=I=-17:TP=-2:LRA=7','-ar',str(rate),'-ac','1','-f','f32le','pipe:1']);a=np.frombuffer(raw,dtype=np.float32);offset=round((cursor+.15)*rate)
  assert len(a)/rate+.15<t['duration'],(i,j)
  voice[offset:offset+len(a)]+=a;cursor+=t['duration']
music=np.zeros_like(voice);chords=[[130.81,164.81,196],[110,130.81,164.81],[87.31,110,130.81],[98,123.47,146.83]]
for k in range(math.ceil(total/.75)):
 onset=k*.75;f=chords[(k//8)%4][k%3]*2;t=np.arange(round(2.8*rate))/rate;a=(np.sin(2*np.pi*f*t)+.22*np.sin(2*np.pi*f*2*t))*np.exp(-t*2.4)*np.minimum(t/.02,1)*.013;at=round(onset*rate);n=min(len(a),len(music)-at)
 if n>0:music[at:at+n]+=a[:n]
idx=np.arange(len(music));music*=np.minimum(idx/rate/2,1)*np.minimum((len(music)-idx)/rate/3,1)
for name,a in [('thuyet-minh',voice),('nhac-nen',music)]:
 subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(rate),'-ac','1','-i','pipe:0','-c:a','libmp3lame','-b:a','128k',str(p/'assets'/(name+'.mp3'))],input=a.astype(np.float32).tobytes(),check=True)
assert abs(voice).max()<1
print('Verified:',sum(map(len,timings)),'sentences; no speech acceleration; duration',total)
