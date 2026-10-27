"""Voice for Speaklo Reels: Kokoro (onnx) + espeak-ng phonemes. Run: python3 voice.py"""
import json,subprocess,sys,wave,os
import numpy as np, onnxruntime as ort
T="/home/claude/tts/"
ESP=T+"inst/bin/espeak-ng"
VOCAB=json.load(open(T+"kokoro-onnx/src/kokoro_onnx/config.json"))["vocab"]
_s=None;_v=None
def _load():
    global _s,_v
    if _s is None:
        _s=ort.InferenceSession(T+"kokoro-v1.0.onnx",providers=["CPUExecutionProvider"])
        _v=np.load(T+"voices-v1.0.bin")
    return _s,_v
def phon(text):
    env=dict(os.environ,ESPEAK_DATA_PATH=T+"inst/share/espeak-ng-data")
    o=subprocess.run([ESP,"-q","--ipa","-v","en-us","--sep=",text],capture_output=True,text=True,env=env).stdout
    o=" ".join(o.split())
    return "".join(c for c in o if c in VOCAB)
def say(text,wav,voice="af_heart",speed=0.9):
    s,v=_load();p=phon(text);tok=[VOCAB[c] for c in p]
    st=v[voice][min(len(tok),len(v[voice]))-1]
    inp={"input_ids" if "input_ids" in [i.name for i in s.get_inputs()] else "tokens":np.array([[0,*tok,0]],dtype=np.int64),"style":st.astype(np.float32),"speed":np.array([speed],dtype=np.float32)}
    a=np.asarray(s.run(None,inp)[0]).ravel()
    a=a/ max(1e-6,np.abs(a).max())*0.9
    with wave.open(wav,"wb") as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes((a*32767).astype(np.int16).tobytes())
    return len(a)/24000
def voice_reel(word,ex,mp4_in,mp4_out,voice="af_heart"):
    """scenes are 3.6s each: 1 word, 2 word again, 3 example, 4 call to action"""
    d="/tmp/vo_"+word;os.makedirs(d,exist_ok=True)
    lines=[(0.5,word+"."),(4.0,word+"."),(7.5,ex),(11.2,"Write your own sentence in the comments.")]
    ins=[];fc=[];ls=[]
    for i,(t,x) in enumerate(lines):
        w=f"{d}/c{i}.wav";dur=say(x,w,voice,0.85 if i<2 else 0.92)
        print(i,x,round(dur,2),"s");assert t+dur<14.3,(x,dur)
        ins+=["-i",w];fc.append(f"[{i+1}:a]adelay={int(t*1000)}|{int(t*1000)},volume=1.0[a{i}]");ls.append(f"[a{i}]")
    f=";".join(fc)+";"+"".join(ls)+f"amix=inputs=4:normalize=0,alimiter=limit=0.95,apad[a]"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",mp4_in]+ins+["-filter_complex",f,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","160k","-t","14.4","-movflags","+faststart",mp4_out],check=True)
if __name__=="__main__":
    R="/home/claude/speaklo-media/reels/"
    voice_reel("support","My family supports me.",R+"2026-10-28_word_support.mp4","/tmp/support_voiced.mp4")
