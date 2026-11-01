from pathlib import Path
import argparse,subprocess,json,re,wave,array,math,tempfile
P=Path(__file__).parent
ap=argparse.ArgumentParser();ap.add_argument('video');args=ap.parse_args();video=Path(args.video)
plan=json.loads((P/'fluent-timing.json').read_text());total=plan['total_duration']
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
assert len(probe['streams'])==2 and abs(float(probe['format']['duration'])-total)<.03
assert sum(s['codec_type']=='audio' for s in probe['streams'])==1
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-af','loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
m=json.loads(re.findall(r'\{[\s\S]*?\}',r.stderr)[-1]);assert abs(float(m['input_i'])+14)<=.1 and float(m['input_tp']) < -1
(P/'final-mp4-loudness.json').write_text(json.dumps(m,indent=2)+'\n')
with tempfile.TemporaryDirectory(prefix='verify-neural-',dir='/tmp') as temp:
 f=Path(temp)/'decoded.wav';subprocess.run(['ffmpeg','-v','error','-i',str(video),'-vn','-ar','48000','-ac','1','-c:a','pcm_s16le',str(f),'-y'],check=True)
 with wave.open(str(f),'rb') as w:samples=array.array('h',w.readframes(w.getnframes()))
 levels=[]
 for scene in plan['scenes']:
  for q in scene['phrases']:
   assert q['end']<=scene['start']+scene['duration'] and q['end']-q['start']>=.5
   a=int((q['start']+.04)*48000);b=int((q['end']-.04)*48000);s=samples[a:b];rms=math.sqrt(sum(v*v for v in s)/len(s))/32768;levels.append(20*math.log10(max(rms,1e-10)))
 assert len(levels)==60 and min(levels)>-45
v=json.loads((P/'verification.json').read_text());v.update({'final_mp4_decoded_entirely':True,'final_mp4_duration_seconds':float(probe['format']['duration']),'final_mp4_audio_streams':1,'final_mp4_frames':int(next(s['nb_frames'] for s in probe['streams'] if s['codec_type']=='video')),'speech_phrases_with_audio_verified':60,'quietest_phrase_rms_dbfs':min(levels),'audio_lufs_integrated':float(m['input_i']),'audio_true_peak_dbtp':float(m['input_tp'])});(P/'verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print('Verified final neural MP4:',m['input_i'],'LUFS,',m['input_tp'],'dBTP, 60 speech phrases; duration',total)
