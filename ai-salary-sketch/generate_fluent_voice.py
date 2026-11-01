from pathlib import Path
import sys,json,time,math
P=Path(__file__).parent
for d in ['neural-tools','neural-runtime','alignment-tools']:sys.path.insert(0,str(P/d))
import numpy as np,soundfile as sf,sherpa_onnx,librosa
D=P/'neural-models/vits-piper-vi_VN-vais1000-medium';OUT=P/'assets/neural';OUT.mkdir(exist_ok=True)
cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=str(next(D.glob('*.onnx'))),tokens=str(D/'tokens.txt'),data_dir=str(D/'espeak-ng-data')),num_threads=3,provider='cpu'),max_num_sentences=4)
assert cfg.validate();tts=sherpa_onnx.OfflineTts(cfg)
texts=json.loads((P/'fluent-script.json').read_text())
repl={'45–50':'bốn mươi lăm đến năm mươi','0 đến 12':'không đến mười hai','12–25':'mười hai đến hai mươi lăm','30–60':'ba mươi đến sáu mươi','55–80':'năm mươi lăm đến tám mươi','70–120':'bảy mươi đến một trăm hai mươi','390–650':'ba trăm chín mươi đến sáu trăm năm mươi'}
def normalize(s):
 for a,b in repl.items():s=s.replace(a,b)
 return s
def speak(s):
 s=normalize(s)
 a=tts.generate(s,sid=0,speed=1.0);assert len(a.samples)>0
 return np.array(a.samples,dtype=np.float32),a.sample_rate,s

def trim(y,sr):
 # Remove only outer silence, keeping a short margin for soft consonants.
 energy=np.sqrt(np.convolve(y.astype(float)**2,np.ones(220)/220,mode='same'));ix=np.flatnonzero(energy>max(.0015,float(energy.max())*.012))
 assert len(ix)>0
 return y[max(0,int(ix[0]-.06*sr)):min(len(y),int(ix[-1]+.10*sr))]

def features(y,sr):
 return librosa.feature.mfcc(y=y,sr=sr,n_mfcc=20,n_fft=512,hop_length=220,n_mels=40,fmin=70,fmax=8000)[1:]

scenes=[];cursor=0;parts=[];spoken_all=[]
for i,group in enumerate(texts):
 start_time=time.monotonic();full,sr,spoken=speak(' '.join(group));full=trim(full,sr);duration=len(full)/sr
 sf.write(str(OUT/f'scene-{i:02}.wav'),full,sr)
 refs=[];bounds=[];n=0
 for j,text in enumerate(group):
  a,ss,s=speak(text);assert ss==sr;a=trim(a,sr);refs.append(a);n+=len(a);bounds.append(n/sr);sf.write(str(OUT/f'ref-{i:02}-{j}.wav'),a,sr)
 ref=np.concatenate(refs)
 X=features(ref,sr);Y=features(full,sr)
 # Acoustic DTW aligns sentence landmarks to the continuous paragraph recording.
 _,path=librosa.sequence.dtw(X=X,Y=Y,metric='cosine',global_constraints=True,band_rad=.22)
 energy=librosa.feature.rms(y=full,frame_length=512,hop_length=220)[0]
 cuts=[]
 for b in bounds[:-1]:
  target=b*sr/220;matched=path[np.abs(path[:,0]-target)<=2,1]
  assert len(matched)>0
  center=float(np.median(matched));lo=max(1,int(center-16));hi=min(len(energy)-1,int(center+17))
  local=energy[lo:hi];low=np.flatnonzero(local<=max(float(local.min())*1.2,.001))
  candidate=lo+int(low[np.argmin(abs((lo+low)-center))]) if len(low) else int(center)
  cuts.append(candidate*220/sr)
 assert 0<cuts[0]<cuts[1]<cuts[2]<duration,(i,cuts,duration)
 edges=[0,*cuts,duration];lead=.85;phrases=[]
 for j,text in enumerate(group):
  phrases.append({'text':text,'spoken':normalize(text),'start':cursor+lead+edges[j],'end':cursor+lead+edges[j+1]})
  assert phrases[-1]['end']-phrases[-1]['start']>=.5
 end_voice=cursor+lead+duration;cut_time=end_voice+.55
 scenes.append({'index':i,'start':cursor,'duration':cut_time-cursor,'voice_start':cursor+lead,'voice_end':end_voice,'phrases':phrases,'dtw_sentence_cuts':cuts})
 parts.append((cursor+lead,full,sr));spoken_all.append(spoken)
 print(f'Scene {i+1:02}: voice {duration:.2f}s, timeline {cut_time:.2f}s; alignment {time.monotonic()-start_time:.1f}s',flush=True)
 cursor=cut_time
# Freeze the ending for 2.6 seconds after the last caption, then fade for 0.8 seconds.
total=math.ceil((scenes[-1]['voice_end']+3.5)*24)/24
assert 180<=total<=300,total
mix=np.zeros(round(total*48000),np.float32)
for start,y,sr in parts:
 y=librosa.resample(y,orig_sr=sr,target_sr=48000);offset=round(start*48000);mix[offset:offset+len(y)]+=y
sf.write(str(P/'assets/narration-neural.wav'),mix,48000,subtype='PCM_24')
plan={'total_duration':total,'voice':'VAIS1000 medium / Piper VITS neural, user-approved sample','generation':'continuous paragraph; no per-phrase stretching or fixed padding','model_release':'https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models','model_file_sha256':'df1512ef3265609f147ae23726b8c8867c6d28e60acb9ffca3545e11783b809f','scenes':scenes}
(P/'fluent-timing.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');(P/'spoken-narration-neural.txt').write_text('\n\n'.join(spoken_all)+'\n')
print('Completed continuous neural voice:',total,'seconds',flush=True)

# Export sentence timing from the continuous audio alignment.
flat=[]
for scene in scenes:
 for j,q in enumerate(scene['phrases']):
  flat.append({'scene':scene['index']+1,'phrase':j+1,'caption':q['text'],'spoken':q['spoken'],'start':q['start'],'end':q['end'],'duration':q['end']-q['start'],'alignment':'MFCC-DTW from paragraph audio'})
(P/'voice-plan.json').write_text(json.dumps(flat,ensure_ascii=False,indent=2)+'\n')
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{(ms//60000)%60:02}:{(ms//1000)%60:02},{ms%1000:03}'
(P/'phu-de-vi.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(q["start"])} --> {stamp(q["end"])}\n{q["caption"]}' for i,q in enumerate(flat))+'\n')
(P/'spoken-narration.txt').write_text('\n\n'.join(spoken_all)+'\n')
