"""Speaklo 'voice Short' auto renderer (v3): user voiceover -> hook scene, 1..n card scenes, CTA scene.
cfg module provides: VOICE (24k mono wav), CHIP, TOTAL, SEGS, ROWS, SCENES, optional SFX_EXTRA.
SCENES=[("hook",a,b,dict(emoji=,lines=[(text,size,color,is_ar)])),("cards",a,b,[row indexes]),("cta",a,b)]
usage: [FB=1] python short_auto.py cfg_module out.mp4"""
import sys,math,importlib,os,subprocess
sys.path.insert(0,'/home/claude/gen')
from fx import *
from short_lib import prop,isar,caption,row
NAME="Speaklo"
FB=bool(os.environ.get("FB"))
POS={1:(560,),2:(430,790),3:(300,625,950)}
def hook(L,T,lt,h):
    s=ease_out_back(lt/0.5);em=emoji(h["emoji"],300);e=em.resize((max(1,int(em.width*s)),max(1,int(em.height*s))),Image.LANCZOS);L.paste(e,(540-e.width//2,520-e.height//2),e)
    t=Image.new("RGBA",(W,520),(0,0,0,0));td=ImageDraw.Draw(t);y=90
    for txt,size,col,isa in h["lines"]:
        if isa:ar(td,(540,y),txt,size,col,"ExtraBold")
        else:
            f=LA(size);td.text((540,y),txt,font=f,fill=col,anchor="mm")
        y+=int(size*1.25)
    t=fade(t,clamp((lt-0.2)/0.3));L.paste(t,(0,800),t)
def cards(C,L,T,idxs):
    for i,y in zip(idxs,POS[len(idxs)]):row(C,L,T,i,y)
def cta(L,T,lt):
    for em,cx,t0 in ((emoji("👥" if FB else "🔔",230),400,0.05),(emoji("👍",230),680,0.35)):
        s=max(0.05,ease_out_back((lt-t0)/0.5)*(1+0.04*math.sin(T*6)));e=em.resize((int(em.width*s),int(em.height*s)),Image.LANCZOS);L.paste(e,(cx-e.width//2,360-e.height//2),e)
    a=clamp((lt-0.1)/0.3);sp=Image.new("RGBA",(W,700),(0,0,0,0));sd=ImageDraw.Draw(sp)
    sd.text((540,70),NAME,font=LA(150),fill=YEL,anchor="mm");ar(sd,(540,230),"تابع الصفحة" if FB else "اشترك في القناة",96,CREAM,"ExtraBold");ar(sd,(540,345),"واعمل لايك",78,YEL,"Bold")
    pul=1+0.05*math.sin(T*7);bw,bh=int(520*pul),int(110*pul);sd.rounded_rectangle((540-bw//2,520-bh//2,540+bw//2,520+bh//2),bh//2,fill=CORAL);sd.text((540,520),"Follow" if FB else "Subscribe",font=LA(58),fill=CREAM,anchor="mm")
    sp=fade(sp,a);L.paste(sp,(0,500),sp)
def scene_layer(C,T,k):
    L=Image.new("RGBA",(W,H),(0,0,0,0));kind,a,b,*rest=C.SCENES[k];lt=T-a
    if kind=="hook":hook(L,T,lt,rest[0])
    elif kind=="cards":cards(C,L,T,rest[0])
    else:cta(L,T,lt)
    return L
def sfx(C):
    out=[(0.1,pop())]
    for r in C.ROWS:out.append((r[4],pop()))
    for k,(kind,a,b,*_) in enumerate(C.SCENES):
        if k>0:out.append((a-0.25,whoosh()))
        if kind=="cta":out+=[(a+0.05,pop()),(a+0.35,pop())]
    return out+list(getattr(C,"SFX_EXTRA",[]))
def main(cfg,out):
    C=importlib.import_module(cfg) if isinstance(cfg,str) else cfg;BG=make_bg();tmp="/tmp/auto_"+os.path.basename(out)
    subprocess.run(["ffmpeg","-y","-v","error","-i",C.VOICE,"-af","loudnorm=I=-17:TP=-3:LRA=9","-ar","24000","-ac","1",tmp+"_v.wav"],check=True)
    mix(C.TOTAL,[(0.0,tmp+"_v.wav")],sfx(C),tmp+"_m.wav")
    subprocess.run(["ffmpeg","-y","-v","error","-i",tmp+"_m.wav","-af","alimiter=limit=0.8:level=0","-ar","24000",tmp+"_f.wav"],check=True)
    chip=Image.new("RGBA",(W,300),(0,0,0,0));cd=ImageDraw.Draw(chip);cw=AR(44,"Bold").getlength(C.CHIP,direction="rtl",language="ar")+80
    cd.rounded_rectangle((60,130,60+cw,210),40,fill=YEL);ar(cd,(60+cw/2,170),C.CHIP,44,NAVY)
    cd.rounded_rectangle((720,130,1000,210),40,fill=NAVY+(215,),outline=YEL+(255,),width=3);cd.text((860,170),NAME,font=LA(40),fill=CREAM,anchor="mm")
    def frame(T):
        im=bg_frame(BG,T).convert("RGBA");k=max(i for i,s in enumerate(C.SCENES) if T>=s[1]-1e-6)
        a,b=C.SCENES[k][1],C.SCENES[k][2];al=min(clamp((T-a)/0.25) if k>0 else 1,clamp((b-T)/0.2) if k<len(C.SCENES)-1 else 1)
        lay=fade(scene_layer(C,T,k),al);im.paste(lay,(0,0),lay);im.paste(chip,(0,0),chip)
        caption(C,im,T);im=im.convert("RGB");progress(im,T,C.TOTAL);return im
    encode(C.TOTAL,frame,tmp+"_f.wav",out)
if __name__=="__main__":main(sys.argv[1],sys.argv[2])
