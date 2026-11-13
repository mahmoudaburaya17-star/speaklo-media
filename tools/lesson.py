"""Speaklo voiced LESSON Reel (short sourced grammar lesson, narrator voice).
make(hook_ar, hook_en, title_ar, sub_en, items, cta_ar, cta_en_voice, out)
items=[(keyword_en, meaning_ar, example_en, example_ar, emoji, (r,g,b), dark_text_bool)]"""
import sys,math,subprocess,wave,os
sys.path.insert(0,'/home/claude/gen')
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import voice
NAVY=(27,42,78);PANEL=(38,56,100);YEL=(255,201,60);CORAL=(255,107,74);MINT=(46,196,182);CREAM=(255,248,238)
FD="/usr/share/fonts/truetype/google-fonts/";G="/home/claude/gen/"
def LA(s,w="Bold"):return ImageFont.truetype(FD+f"Poppins-{w}.ttf",s)
def AR(s,w="Medium"):return ImageFont.truetype(G+f"Tajawal-{w}.ttf",s,layout_engine=ImageFont.Layout.RAQM)
W,H,FPS=1080,1920,24
def emoji(ch,size=260):
    f=ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",109)
    im=Image.new("RGBA",(136,128),(0,0,0,0));ImageDraw.Draw(im).text((0,0),ch,font=f,embedded_color=True)
    return im.resize((int(136*size/128),size),Image.LANCZOS)
def wrap(d,t,f,mw):
    out=[];cur=""
    for w in t.split():
        n=(cur+" "+w).strip()
        if d.textlength(n,font=f)<=mw:cur=n
        else:out.append(cur);cur=w
    return out+[cur]
def ar(d,xy,t,size,fill,w="Bold",anchor="mm"):
    d.text(xy,t,font=AR(size,w),fill=fill,anchor=anchor,direction="rtl",language="ar")
def frame(title,sub,n,idx):
    im=Image.new("RGB",(W,H),NAVY);d=ImageDraw.Draw(im)
    d.rounded_rectangle((60,70,330,150),40,fill=YEL);ar(d,(195,110),"درس سريع",44,NAVY)
    ar(d,(540,240),title,78,YEL,"ExtraBold");d.text((540,325),sub,font=LA(36,"Medium"),fill=CREAM,anchor="mm")
    for i in range(n):
        cx=540+(i-(n-1)/2)*50;r=14
        d.ellipse((cx-r,400-r,cx+r,400+r),fill=YEL if i==idx else PANEL)
    d.text((540,1865),"Speaklo  ·  Speak it. Own it.",font=LA(30,"Medium"),fill=(150,165,200),anchor="mm")
    return im,d
def fit(d,t,maxw,start=120):
    s=start
    while d.textlength(t,font=LA(s))>maxw and s>40:s-=4
    return LA(s)
def item_base(title,sub,n,idx,it):
    kw,mean,ex,exar,em,col,dark=it
    im,d=frame(title,sub,n,idx);tc=NAVY if dark else CREAM
    d.rounded_rectangle((100,470,980,1130),56,fill=col)
    d.text((540,830),kw,font=fit(d,kw,780),fill=tc,anchor="mm")
    ar(d,(540,985),mean,62,tc)
    d.rounded_rectangle((60,1190,1020,1700),48,fill=PANEL)
    d.rounded_rectangle((90,1160,260,1222),31,fill=YEL);ar(d,(175,1191),"مثال",36,NAVY)
    fe=LA(62);y=1280
    for l in wrap(d,ex,fe,880):d.text((100,y),l,font=fe,fill=CREAM);y+=84
    ar(d,(540,y+70),exar,54,YEL,"Medium","ma")
    return im
def hook_base(hook_ar,hook_en):
    im=Image.new("RGB",(W,H),NAVY);d=ImageDraw.Draw(im)
    d.rounded_rectangle((60,70,330,150),40,fill=YEL);ar(d,(195,110),"درس سريع",44,NAVY)
    ar(d,(540,760),hook_ar[0],104,YEL,"ExtraBold");ar(d,(540,900),hook_ar[1],104,CREAM,"ExtraBold")
    d.text((540,1090),hook_en,font=LA(52,"Bold"),fill=MINT,anchor="mm")
    d.text((540,1865),"Speaklo  ·  Speak it. Own it.",font=LA(30,"Medium"),fill=(150,165,200),anchor="mm")
    return im
def cta_base(lines):
    im=Image.new("RGB",(W,H),NAVY);d=ImageDraw.Draw(im)
    d.rounded_rectangle((60,70,330,150),40,fill=YEL);ar(d,(195,110),"درس سريع",44,NAVY)
    y=700
    for i,l in enumerate(lines):
        ar(d,(540,y),l,74 if i==0 else 58,YEL if i==0 else CREAM,"ExtraBold" if i==0 else "Bold");y+=130 if i==0 else 100
    d.text((540,1865),"Speaklo  ·  Speak it. Own it.",font=LA(30,"Medium"),fill=(150,165,200),anchor="mm")
    return im
def make(hook_ar,hook_en,hook_voice,title,sub,items,cta_lines,cta_voice,out,src="/tmp/lesson"):
    os.makedirs(src,exist_ok=True);sr=24000;t=0.3;ev=[]
    w=f"{src}/h.wav";du=voice.say(hook_voice,w,"bf_emma",0.9);ev.append((t,du+0.5,w,hook_base(hook_ar,hook_en),emoji("🤔"),None));t+=du+0.9
    n=len(items)
    for i,it in enumerate(items):
        w=f"{src}/i{i}.wav";txt=it[0].replace("'","’") if False else it[0]
        du=voice.say(f"{it[0]}. {it[2]}",w,"bf_emma",0.9);ev.append((t,du+0.4,w,item_base(title,sub,n,i,it),emoji(it[4]),it));t+=du+0.8
    w=f"{src}/c.wav";du=voice.say(cta_voice,w,"bf_emma",0.9);ev.append((t,du+1.0,w,cta_base(cta_lines),emoji("👍"),None));t+=du+1.2
    total=t;aud=np.zeros(int(total*sr)+sr)
    for s,dur,wv,_,_,_ in ev:
        x=np.frombuffer(wave.open(wv).readframes(10**8),dtype=np.int16)/32768;a=int(s*sr);aud[a:a+len(x)]+=x
    wv=f"{src}/all.wav"
    with wave.open(wv,"wb") as o:o.setnchannels(1);o.setsampwidth(2);o.setframerate(sr);o.writeframes((np.clip(aud,-1,1)*32767).astype(np.int16).tobytes())
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",wv,"-c:v","libx264","-pix_fmt","yuv420p","-preset","fast","-crf","20","-c:a","aac","-b:a","160k","-t",f"{total:.2f}","-movflags","+faststart",out],stdin=subprocess.PIPE)
    for fr in range(int(total*FPS)):
        T=fr/FPS;cur=[e for e in ev if e[0]<=T+0.05];e=cur[-1] if cur else ev[0]
        im=e[3].copy();em=e[4];cy=(640 if e[5] else 440)
        if e[5] is None and e is ev[0]:cy=420
        if e[5]: cy=640
        im.paste(em,(540-em.width//2,cy-em.height//2+int(10*math.sin(T*3))),em)
        p.stdin.write(im.tobytes())
    p.stdin.close();p.wait();return total
