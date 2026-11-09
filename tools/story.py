"""Speaklo voiced story Reel: narrator + Sara + Adam, scene card with emoji, EN+AR subtitle, end card with 3 words.
usage: story.make(title_ar, sub_en, scenes, words, out_mp4)
scenes=[(speaker 'N'|0|1, english, arabic, emoji, (r,g,b) card colour)]; words=[(EN, AR)]"""
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
VOICES={"N":"bf_emma",0:"af_heart",1:"am_adam"}
NAMES={"N":"Narrator",0:"Sara",1:"Adam"}
CHC={0:CORAL,1:MINT}
EMO=None
def emoji(ch,size=420):
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
def header(d,title,sub):
    d.rounded_rectangle((60,70,260,150),40,fill=YEL);d.text((160,110),"قصة",font=AR(44,"Bold"),fill=NAVY,anchor="mm",direction="rtl",language="ar")
    d.text((540,235),title,font=AR(78,"ExtraBold"),fill=YEL,anchor="mm",direction="rtl",language="ar")
    d.text((540,320),sub,font=LA(38,"Medium"),fill=CREAM,anchor="mm")
def avatars(d,act,T):
    for sp,cx in ((0,300),(1,780)):
        r=85*(1+(0.07*math.sin(T*14) if act==sp else 0));cy=1130
        if act==sp:d.ellipse((cx-r-14,cy-r-14,cx+r+14,cy+r+14),outline=YEL,width=8)
        d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=CHC[sp]);d.text((cx,cy),NAMES[sp][0],font=LA(90),fill=NAVY if sp==1 else CREAM,anchor="mm")
        d.text((cx,cy+125),NAMES[sp],font=LA(36),fill=CREAM,anchor="mm")
def scene_base(title,sub,sp,en,ar,col):
    im=Image.new("RGB",(W,H),NAVY);d=ImageDraw.Draw(im);header(d,title,sub)
    d.rounded_rectangle((140,400,940,980),48,fill=col)
    d.rounded_rectangle((60,1330,1020,1830),44,fill=PANEL)
    lab=NAMES[sp];c=CHC.get(sp,YEL)
    d.rounded_rectangle((90,1300,90+40+int(d.textlength(lab,font=LA(36))),1362),31,fill=c);d.text((110,1331),lab,font=LA(36),fill=NAVY if sp!=0 else CREAM,anchor="lm")
    fe=LA(52);y=1400
    for l in wrap(d,en,fe,880):d.text((100,y),l,font=fe,fill=CREAM);y+=70
    d.text((540,y+50),ar,font=AR(46),fill=YEL,anchor="ma",direction="rtl",language="ar")
    return im
def end_base(title,words):
    im=Image.new("RGB",(W,H),NAVY);d=ImageDraw.Draw(im);header(d,title,"New words")
    d.text((540,470),"كلمات القصة",font=AR(70,"ExtraBold"),fill=CREAM,anchor="mm",direction="rtl",language="ar")
    for i,(en,ar) in enumerate(words):
        y=580+i*250;d.rounded_rectangle((90,y,990,y+210),44,fill=[CORAL,MINT,YEL][i%3])
        tc=CREAM if i%3==0 else NAVY
        d.text((540,y+75),en.upper(),font=LA(80),fill=tc,anchor="mm");d.text((540,y+153),ar,font=AR(56,"Bold"),fill=tc,anchor="mm",direction="rtl",language="ar")
    d.text((540,1450),"اكتب جملتك بواحدة منهم",font=AR(54,"Bold"),fill=YEL,anchor="mm",direction="rtl",language="ar")
    d.text((540,1530),"في الكومنتات",font=AR(54,"Bold"),fill=YEL,anchor="mm",direction="rtl",language="ar")
    return im
def make(title,sub,scenes,words,out):
    d="/tmp/story";os.makedirs(d,exist_ok=True);sr=24000;t=0.8;ev=[]
    for i,(sp,en,ar,em,col) in enumerate(scenes):
        w=f"{d}/l{i}.wav";du=voice.say(en,w,VOICES[sp],0.9)
        ev.append((t,du,sp,w,scene_base(title,sub,sp,en,ar,col),emoji(em)));t+=du+0.6
    wt=t+0.3;ww=[]
    for i,(en,ar) in enumerate(words):
        w=f"{d}/w{i}.wav";du=voice.say(en+".",w,VOICES["N"],0.8);ww.append((wt,du,w));wt+=du+0.9
    cta=f"{d}/cta.wav";cdu=voice.say("Write your own sentence in the comments.",cta,VOICES["N"],0.9);ww.append((wt,cdu,cta))
    total=wt+cdu+1.2;endt=ev[-1][0]+ev[-1][1]+0.5
    aud=np.zeros(int(total*sr)+sr)
    for s,du,w in [(e[0],e[1],e[3]) for e in ev]+ww:
        x=np.frombuffer(wave.open(w).readframes(10**8),dtype=np.int16)/32768;a=int(s*sr);aud[a:a+len(x)]+=x
    wv=f"{d}/all.wav"
    with wave.open(wv,"wb") as o:o.setnchannels(1);o.setsampwidth(2);o.setframerate(sr);o.writeframes((np.clip(aud,-1,1)*32767).astype(np.int16).tobytes())
    eb=end_base(title,words)
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",wv,"-c:v","libx264","-pix_fmt","yuv420p","-preset","fast","-crf","20","-c:a","aac","-b:a","160k","-t",f"{total:.2f}","-movflags","+faststart",out],stdin=subprocess.PIPE)
    for fr in range(int(total*FPS)):
        T=fr/FPS
        if T>=endt:
            im=eb.copy();dr=ImageDraw.Draw(im)
            for i,(s,du,_) in enumerate(ww[:-1]):
                if T<s:
                    y=580+i*250;dr.rounded_rectangle((90,y,990,y+210),44,fill=NAVY)
        else:
            cur=[e for e in ev if e[0]<=T];e=cur[-1] if cur else ev[0]
            im=e[4].copy();dr=ImageDraw.Draw(im)
            act=e[2] if (e[0]<=T<e[0]+e[1]) else None
            avatars(dr,act if act in (0,1) else None,T)
            em=e[5];im.paste(em,(540-em.width//2,690-em.height//2+int(10*math.sin(T*3))),em)
        p.stdin.write(im.tobytes())
    p.stdin.close();p.wait();return total
if __name__=="__main__":
    S=[("N","One morning, Sara finds a wallet on the street.","في صباح يوم، سارة لقت محفظة في الشارع.","👛",(46,196,182)),
    (0,"Oh no! Someone lost this wallet.","يا نهار! حد ضيّع المحفظة دي.","😮",(255,107,74)),
    ("N","There is a card inside. It has a phone number.","جواها كارت عليه رقم تليفون.","📇",(255,201,60)),
    (0,"Hello? I found your wallet.","ألو؟ أنا لقيت محفظتك.","📞",(255,107,74)),
    (1,"Really? Thank you so much! I was very worried.","بجد؟ شكراً جداً! كنت قلقان أوي.","😟",(46,196,182)),
    ("N","They meet at the café.","اتقابلوا في الكافيه.","☕",(255,201,60)),
    (1,"Here is a reward for you.","اتفضلي مكافأة ليكي.","💵",(46,196,182)),
    (0,"No, thank you. I only did the right thing.","لا شكراً. أنا عملت الصح بس.","🙂",(255,107,74)),
    ("N","Adam smiles. Sara is a very honest person.","آدم ابتسم. سارة إنسانة أمينة جداً.","😊",(255,201,60))]
    W3=[("wallet","محفظة"),("honest","أمين"),("reward","مكافأة")]
    print(make("المحفظة الضايعة","The Lost Wallet",S,W3,"/home/claude/speaklo-media/reels/2026-11-10_story_lost_wallet.mp4"))
