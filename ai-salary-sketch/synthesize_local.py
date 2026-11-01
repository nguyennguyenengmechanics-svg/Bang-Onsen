from pathlib import Path
import ctypes as C,wave,json,re
P=Path(__file__).parent
LIB=P/'voice-tools/espeakng_loader/libespeak-ng.so.1'
lib=C.CDLL(str(LIB))
lib.espeak_Initialize.argtypes=[C.c_int,C.c_int,C.c_char_p,C.c_int];lib.espeak_Initialize.restype=C.c_int
sr=lib.espeak_Initialize(2,0,str(LIB.parent).encode(),0)
assert sr>0,sr
CB=C.CFUNCTYPE(C.c_int,C.POINTER(C.c_short),C.c_int,C.c_void_p)
chunks=[]
@CB
def callback(wav,n,events):
 if bool(wav) and n>0:chunks.append(C.string_at(wav,n*2))
 return 0
lib.espeak_SetSynthCallback.argtypes=[CB];lib.espeak_SetSynthCallback(callback)
lib.espeak_SetVoiceByName.argtypes=[C.c_char_p];lib.espeak_SetVoiceByName.restype=C.c_int
assert lib.espeak_SetVoiceByName(b'vi')==0
lib.espeak_SetParameter.argtypes=[C.c_int,C.c_int,C.c_int]
lib.espeak_SetParameter(1,205,0);lib.espeak_SetParameter(2,90,0);lib.espeak_SetParameter(3,48,0)
lib.espeak_Synth.argtypes=[C.c_void_p,C.c_size_t,C.c_uint,C.c_int,C.c_uint,C.c_uint,C.POINTER(C.c_uint),C.c_void_p]
lib.espeak_Synth.restype=C.c_int
lib.espeak_Synchronize.restype=C.c_int

def synth(text,path,rate=205):
 chunks.clear();lib.espeak_SetParameter(1,rate,0);b=text.encode('utf-8')+b'\0';buf=C.create_string_buffer(b)
 err=lib.espeak_Synth(buf,len(b),0,1,0,1,None,None);assert err==0,err;lib.espeak_Synchronize()
 pcm=b''.join(chunks)
 with wave.open(str(path),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(pcm)
 return len(pcm)/2/sr
if __name__=='__main__':
 out=P/'assets/voice-sample.wav';print('Vietnamese voice sample:',synth('Xin chào. Đây là video về mức lương kỹ sư trí tuệ nhân tạo.',out), 'seconds; sample rate',sr)
