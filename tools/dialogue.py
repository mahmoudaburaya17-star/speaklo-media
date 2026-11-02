"""Speaklo motion dialogue: two voiced characters, chat bubbles pop in, EN + AR on screen.
usage: dialogue.make(title_ar, sub_en, lines, out_mp4); lines=[(speaker 0/1, english, arabic)]"""
import sys,math,subprocess,wave,os
sys.path.insert(0,'/home/claude/gen')
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import voice
NAVY=(27,42,78);YEL=(255,201,60);CORAL=(255,107,74);MINT=(46,196,182);CREAM=(255,248,238)
FD="/usr/share/fonts/truetype/google-fonts/";G="/home/claude/gen/"
def LA(s,w="Bold"):return ImageFont.truetype(FD+f"Poppins-{w}.ttf",s)
def AR(s,w="Medium"):return ImageFont.truetype(G+f"Tajawal-{w}.ttf",s,layout_engine=ImageFont.Layout.RAQM)
W,H,FPS=1080,1920,20
CH=[dict(name="Sara",voice="af_heart",col=CORAL,txt=CREAM),dict(name="Adam",voice="am_adam",col=MINT,txt=NAVY)]
def wrap(d,t,f,mw):
    out=[];cur=""
    for w in t.split():
        n=(cur+" "+w).strip()
        if d.textlength(n,font=f)<=mw:cur=n
        else:out.append(cur);cur=w
    return out+[cur]
def bubble(sp,en,ar):
    d0=ImageDraw.Draw(Image.new("RGB",(10,10)));fe=LA(46);fa=AR(40)
    el=wrap(d0,en,fe,740);bw=max(int(max(d0.textlength(l,font=fe) for l in el)),int(d0.textlength(ar,font=fa,direction="rtl",language="ar")))+80
    h=50+len(el)*64+20+56+30
    im=Image.new("RGBA",(bw,h),(0,0,0,0));d=ImageDraw.Draw(im);c=CH[sp]
    d.rounded_rectangle((0,0,bw-1,h-1),44,fill=c["col"]);y=40
    for l in el:d.text((40,y),l,font=fe,fill=c["txt"]);y+=64
    d.text((bw/2,y+22),ar,font=fa,fill=c["txt"],anchor="ma",direction="rtl",language="ar")
    return im
def make(title_ar,sub_en,lines,out):
    d="/tmp/dlg";os.makedirs(d,exist_ok=True);sr=24000;t=1.0;ev=[]
    for i,(sp,en,ar) in enumerate(lines):
        w=f"{d}/l{i}.wav";du=voice.say(en,w,CH[sp]["voice"],0.9);ev.append((t,du,sp,w,bubble(sp,en,ar)));t+=du+0.7
    total=t+2.5;aud=np.zeros(int(total*sr)+sr)
    for s,du,sp,w,_ in ev:
        x=np.frombuffer(wave.open(w).readframes(10**8),dtype=np.int16)/32768;a=int(s*sr);aud[a:a+len(x)]+=x
    wv=f"{d}/all.wav"
    with wave.open(wv,"wb") as o:o.setnchannels(1);o.setsampwidth(2);o.setframerate(sr);o.writeframes((np.clip(aud,-1,1)*32767).astype(np.int16).tobytes())
    ft=AR(84,"ExtraBold");fs=LA(40,"Medium");fc=AR(48,"Bold")
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",wv,"-c:v","libx264","-pix_fmt","yuv420p","-preset","fast","-crf","20","-c:a","aac","-b:a","160k","-t",f"{total:.2f}","-movflags","+faststart",out],stdin=subprocess.PIPE)
    for fr in range(int(total*FPS)):
        T=fr/FPS;im=Image.new("RGB",(W,H),NAVY);dr=ImageDraw.Draw(im)
        dr.rounded_rectangle((60,70,300,150),40,fill=YEL);dr.text((180,110),"محادثة",font=AR(44,"Bold"),fill=NAVY,anchor="mm",direction="rtl",language="ar")
        dr.text((540,300),title_ar,font=ft,fill=YEL,anchor="mm",direction="rtl",language="ar")
        dr.text((540,390),sub_en,font=fs,fill=CREAM,anchor="mm")
        act=None
        for s,du,sp,_,_ in ev:
            if s<=T<s+du:act=sp
        for sp,cx in ((0,300),(1,780)):
            r=105*(1+(0.07*math.sin(T*14) if act==sp else 0));cy=620
            if act==sp:dr.ellipse((cx-r-14,cy-r-14,cx+r+14,cy+r+14),outline=YEL,width=8)
            dr.ellipse((cx-r,cy-r,cx+r,cy+r),fill=CH[sp]["col"])
            dr.text((cx,cy),CH[sp]["name"][0],font=LA(110),fill=CH[sp]["txt"],anchor="mm")
            dr.text((cx,cy+150),CH[sp]["name"],font=LA(40),fill=CREAM,anchor="mm")
        vis=[e for e in ev if e[0]<=T][-3:];y=840
        for k,(s,du,sp,_,b) in enumerate(vis):
            age=T-s;pop=min(1,age/0.25);oy=int((1-pop)*40);old=(k<len(vis)-1)
            bi=b.copy();al=int(255*pop*(0.5 if old else 1));bi.putalpha(bi.getchannel("A").point(lambda v:v*al//255))
            x=60 if sp==0 else W-60-b.width;im.paste(bi,(x,y+oy),bi);y+=b.height+40
        if T>total-2.5:
            dr.text((540,1800),"جرّب المحادثة دي مع صاحبك!",font=fc,fill=YEL,anchor="mm",direction="rtl",language="ar")
        p.stdin.write(im.tobytes())
    p.stdin.close();p.wait();return total
if __name__=="__main__":
    L=[(0,"Hi! Can I help you?","أهلاً! أقدر أساعدك؟"),
       (1,"Yes, please. I would like a coffee.","أيوه لو سمحت. عايز قهوة."),
       (0,"Sure. Do you want milk?","أكيد. عايز لبن؟"),
       (1,"No, thank you. Just black.","لا شكراً. سادة بس."),
       (0,"Here you go.","اتفضل."),
       (1,"Thank you very much!","شكراً جداً!")]
    print(make("في الكافيه","At the café",L,"/home/claude/gen/dialogue_cafe.mp4"))
