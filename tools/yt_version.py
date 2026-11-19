"""Speaklo YouTube version of a Facebook Reel (user rule 2026-11-18: channel name inside the video + subscribe/like CTA).
make(in_mp4, out_mp4): finds the start of the Facebook CTA scene (biggest frame jump in the last 9 s), cuts there,
appends a YouTube end card (Speaklo name, bell + thumbs-up, 'اشترك في القناة واعمل لايك', voiced 'Like and subscribe to Speaklo!'),
and burns a small 'Speaklo' name pill (top-right, inside the safe zone) over the whole video.
Needs /home/claude/gen (fx.py, Tajawal fonts) and the TTS stack (voice.py). Peak check after encode is still your job."""
import sys,os,subprocess,numpy as np
sys.path.insert(0,'/home/claude/gen')
from fx import *
import voice
NAME="Speaklo"
def find_cta_start(mp4,win=9.0):
    dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",mp4]))
    st=max(0,dur-win);w,h=108,192
    raw=subprocess.check_output(["ffmpeg","-v","error","-ss",f"{st:.3f}","-i",mp4,"-an","-vf",f"fps=24,scale={w}:{h},format=gray","-f","rawvideo","-"])
    fr=np.frombuffer(raw,dtype=np.uint8).reshape(-1,h,w).astype(np.int16)
    d=np.abs(np.diff(fr,axis=0)).mean(axis=(1,2));i=int(d.argmax())+1
    return st+i/24.0,dur
def watermark(path):
    im=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rounded_rectangle((720,130,1000,210),40,fill=NAVY+(215,),outline=YEL+(255,),width=3)
    d.text((860,170),NAME,font=LA(40),fill=CREAM,anchor="mm");im.save(path)
MODES={"yt":dict(say="Like and subscribe to {n}!",icons=("🔔","👍"),l1="اشترك في القناة",l2="واعمل لايك",btn="Subscribe"),
       "fb":dict(say="Follow {n} for a new English lesson every day!",icons=("👍","👥"),l1="تابع الصفحة",l2="واعمل لايك وابعتها لصاحبك",btn="Follow")}
def end_card(Tc,out,tmp,mode="yt"):
    M=MODES[mode]
    cv=voice.say(M["say"].format(n=NAME),f"{tmp}/yt_cta.wav","bf_emma",0.9)
    dur=cv+1.6;voices=[(0.5,f"{tmp}/yt_cta.wav")];sfx=[(0.05,pop()),(0.35,pop()),(0.65,pop())]
    mix(dur,voices,sfx,f"{tmp}/yt_all.wav");BG=make_bg();bell=emoji(M["icons"][0],230);thumb=emoji(M["icons"][1],230)
    total=Tc+dur
    def frame(t):
        T=Tc+t;im=bg_frame(BG,T);d=ImageDraw.Draw(im)
        for k,(em,cx,t0) in enumerate(((bell,400,0.05),(thumb,680,0.35))):
            s=max(0.05,ease_out_back((t-t0)/0.5)*(1+0.04*math.sin(T*6)));e=em.resize((int(em.width*s),int(em.height*s)),Image.LANCZOS);im.paste(e,(cx-e.width//2,560-e.height//2),e)
        a=clamp((t-0.1)/0.3);sp=Image.new("RGBA",(W,700),(0,0,0,0));sd=ImageDraw.Draw(sp)
        sd.text((540,70),NAME,font=LA(140),fill=YEL,anchor="mm");ar(sd,(540,230),M["l1"],96,CREAM,"ExtraBold");ar(sd,(540,345),M["l2"],78 if mode=="yt" else 60,YEL,"Bold")
        pul=1+0.05*math.sin(T*7);bw,bh=int(520*pul),int(110*pul);sd.rounded_rectangle((540-bw//2,520-bh//2,540+bw//2,520+bh//2),bh//2,fill=CORAL);sd.text((540,520),M["btn"],font=LA(58),fill=CREAM,anchor="mm")
        sp=fade(sp,a);im.paste(sp,(0,760),sp);progress(im,T,total);return im
    encode(dur,frame,f"{tmp}/yt_all.wav",out)
    return dur
def make(in_mp4,out_mp4,tmp="/tmp/ytv",mode="yt"):
    os.makedirs(tmp,exist_ok=True);Tc,dur=find_cta_start(in_mp4)
    end_card(Tc,f"{tmp}/endcard.mp4",tmp,mode);watermark(f"{tmp}/wm.png")
    fg=(f"[0:v]trim=0:{Tc:.3f},setpts=PTS-STARTPTS,fps=24[v0];[0:a]atrim=0:{Tc:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={max(0,Tc-0.15):.3f}:d=0.15,aresample=48000[a0];"
        "[1:v]fps=24,setpts=PTS-STARTPTS[v1];[1:a]aresample=48000[a1];[v0][v1]concat=n=2:v=1:a=0[vc];[a0][a1]concat=n=2:v=0:a=1,alimiter=limit=0.8:level=disabled[a];[vc][2:v]overlay=0:0[v]")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",in_mp4,"-i",f"{tmp}/endcard.mp4","-i",f"{tmp}/wm.png","-filter_complex",fg,"-map","[v]","-map","[a]",
                    "-c:v","libx264","-pix_fmt","yuv420p","-preset","fast","-crf","19","-c:a","aac","-b:a","160k","-movflags","+faststart",out_mp4],check=True)
    return Tc,dur
if __name__=="__main__":
    print(make(sys.argv[1],sys.argv[2],mode=(sys.argv[3] if len(sys.argv)>3 else "yt")))
