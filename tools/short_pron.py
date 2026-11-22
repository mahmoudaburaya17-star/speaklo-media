"""Speaklo YouTube Short from a user-supplied voiceover (silent letters / pronunciation).
Voiceover segments were measured from the audio (energy envelope), word timing inside a phrase is proportional to word length.
usage: python short_pron.py out.mp4   (needs /tmp/vo.wav = 24 kHz mono wav of the voiceover)"""
import sys,math
sys.path.insert(0,'/home/claude/gen')
from fx import *
DJ="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
NAME="Speaklo"
SEG=[(0.14,1.66),(2.00,2.98),(3.44,6.04),(6.24,7.50),(7.88,8.42),(8.82,9.38),(9.86,10.42),(11.06,12.32),(12.68,13.74),(14.24,14.72),(15.28,16.56),(16.88,17.94),(18.28,18.80),(19.56,21.56),(21.76,23.54)]
# caption phrase per segment (None = pure English word, the card shows it)
CAP=["لو بتقول ويدنزداي…","الفيديو ده ليك","كلمة Wednesday فيها حرف D ساكن خالص","مش ويدنزداي",None,"قولها معايا:",None,"نفس الحكاية في Comfortable","مش كومفورتيبل",None,"وآخر واحدة: Vegetable","مش فيجيتيبل",None,"تابع Speaklo عشان كل يوم كلمة جديدة","واكتب في الكومنتات كلمة نطقها واقف معاك"]
SCN=[(0,3.2),(3.2,10.74),(10.74,15.0),(15.0,19.18),(19.18,26.4)]
TOTAL=26.4
def isar(w):return any("؀"<=c<="ۿ" for c in w)
def wfont(w,s):return AR(s,"Bold") if isar(w) else LA(s)
def wlen(w,s):
    f=wfont(w,s);return f.getlength(w,direction="rtl",language="ar") if isar(w) else f.getlength(w)
def wtimes(i):
    a,b=SEG[i];ws=CAP[i].split();wt=[len(w)+1.5 for w in ws];tot=sum(wt);acc=0;out=[]
    for w,x in zip(ws,wt):out.append((w,a+(b-a)*acc/tot,a+(b-a)*(acc+x)/tot));acc+=x
    return out
WT={i:wtimes(i) for i in range(len(CAP)) if CAP[i]}
def seg_at(T):
    for i,(a,b) in enumerate(SEG):
        if a-0.05<=T<=b+0.35:return i
    return None
def spoken(T,iv):return any(a<=T<=b for a,b in iv)
def caption(im,T):
    i=seg_at(T)
    if i is None or not CAP[i]:return
    a,b=SEG[i];al=min(clamp((T-(a-0.05))/0.12),clamp((b+0.35-T)/0.15))
    ws=WT[i];size=66;maxw=860;lines=[[]];cur=0
    for w,s,e in ws:
        L=wlen(w,size)+22
        if cur+L>maxw and lines[-1]:lines.append([]);cur=0
        lines[-1].append((w,s,e,L));cur+=L
    ov=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(ov)
    ph=len(lines)*104+60;y0=1410-ph//2
    d.rounded_rectangle((70,y0,1010,y0+ph),44,fill=PANEL+(215,),outline=DIM+(90,),width=2)
    for li,ln in enumerate(lines):
        tw=sum(L for _,_,_,L in ln)-22;x=540+tw/2;y=y0+30+52+li*104
        for w,s,e,L in ln:
            wl=wlen(w,size);col=YEL if s<=T<e else (CREAM if T>=e else DIM)
            f=wfont(w,size)
            if isar(w):d.text((x-wl/2,y),w,font=f,fill=col,anchor="mm",direction="rtl",language="ar")
            else:d.text((x-wl/2,y),w,font=f,fill=col,anchor="mm")
            x-=L
    ov=fade(ov,al);im.paste(ov,(0,0),ov)
def pillrow(d,im,y,ok,txt,T,t0,syl=None,segs=()):
    """row with an emoji mark: ok=True -> green check, False -> red cross; pops in at t0"""
    k=clamp((T-t0)/0.35)
    if k<=0:return
    sc=ease_out_back(k);em=emoji("✅" if ok else "❌",84);ex=int(em.width*sc);ey=int(em.height*sc)
    parts=syl if syl else [txt];size=100 if ok else 70;tot=sum(wlen(p,size) for p in parts)+ (len(parts)-1)*0
    x0=540-tot/2+50
    sp=Image.new("RGBA",(W,200),(0,0,0,0));sd=ImageDraw.Draw(sp)
    x=x0;n=len(parts);act=-1
    for a,b in segs:
        if a<=T<=b:act=min(n-1,int((T-a)/(b-a)*n))
    for j,p in enumerate(parts):
        col=(YEL if j==act else MINT) if ok else CORAL
        sd.text((x,100),p,font=LA(size),fill=col,anchor="lm");x+=wlen(p,size)
    sp=fade(sp,k);im.paste(sp,(0,y-100),sp)
    e2=em.resize((max(1,ex),max(1,ey)),Image.LANCZOS);im.paste(e2,(int(x0-70-e2.width/2),int(y-e2.height/2)),e2)
def word_title(d,T,txt,y,size,t0,iv,dtime=None,didx=None):
    k=ease_out_back((T-t0)/0.45)
    if T<t0:return
    f=LA(size);tot=f.getlength(txt);x0=540-tot/2
    hot=spoken(T,iv);col=YEL if hot else CREAM
    if didx is not None and dtime is not None and T>=dtime:
        xs=x0+f.getlength(txt[:didx]);xe=x0+f.getlength(txt[:didx+1]);a=clamp((T-dtime)/0.35)
        d.rounded_rectangle((xs-6,y-size*0.78,xe+6,y+size*0.32),14,fill=CORAL+(int(150*a),))
    for i,c in enumerate(txt):
        x=x0+f.getlength(txt[:i]);cc=col
        if didx==i and dtime is not None and T>=dtime:cc=CORAL if T-dtime>0.25 else CREAM
        d.text((x,y),c,font=f,fill=cc,anchor="ls")
    if didx is not None and dtime is not None and T>=dtime+0.2:
        xs=x0+f.getlength(txt[:didx]);xe=x0+f.getlength(txt[:didx+1]);a=clamp((T-dtime-0.2)/0.3)
        d.line((xs-4,y-size*0.12,xs+(xe-xs+8)*a,y-size*0.12-(0*a)),fill=CREAM,width=8)
def ipa(d,T,txt,y,t0):
    a=clamp((T-t0)/0.4)
    if a<=0:return
    d.text((540,y),txt,font=ImageFont.truetype(DJ,52),fill=tuple(int(DIM[i]*a+PANEL[i]*(1-a)) for i in range(3)),anchor="mm")
def scene_layer(T,k):
    L=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(L);lt=T-SCN[k][0]
    if k==0:
        s=ease_out_back(lt/0.5);em=emoji("🤔",300);e=em.resize((int(em.width*s)+1,int(em.height*s)+1),Image.LANCZOS);L.paste(e,(540-e.width//2,520-e.height//2),e)
        a=clamp((lt-0.35)/0.3);t=Image.new("RGBA",(W,300),(0,0,0,0));td=ImageDraw.Draw(t);ar(td,(540,150),"ويدنزداي؟",190,CORAL,"ExtraBold");t=fade(t,a);L.paste(t,(0,760),t)
        if T>=1.2:
            s=ease_out_back((T-1.2)/0.4);em=emoji("❌",200);e=em.resize((int(em.width*s)+1,int(em.height*s)+1),Image.LANCZOS);L.paste(e,(540-e.width//2,1130-e.height//2),e)
    elif k==1:
        word_title(d,T,"Wednesday",650,130,3.3,[(7.88,8.42),(9.86,10.42),(WT[2][1][1],WT[2][1][2])],WT[2][4][1],2)
        pillrow(d,L,880,False,"Wed-nes-day",T,6.24)
        pillrow(d,L,1030,True,None,T,7.88,syl=["WENZ","-day"],segs=[(7.88,8.42),(9.86,10.42)])
        ipa(d,T,"/ˈwenzdeɪ/",1150,7.9)
        if 8.8<=T<=10.6:
            p=1+0.08*math.sin(T*10);em=emoji("🎤",120);e=em.resize((int(em.width*p),int(em.height*p)),Image.LANCZOS);L.paste(e,(540-e.width//2,1255-e.height//2),e)
    elif k==2:
        word_title(d,T,"Comfortable",650,112,10.9,[(14.24,14.72),(WT[7][3][1],WT[7][3][2])])
        pillrow(d,L,880,False,"com-for-ta-ble",T,12.68)
        pillrow(d,L,1030,True,None,T,14.24,syl=["KUMF","-ter","-bul"],segs=[(14.24,14.72)])
        ipa(d,T,"/ˈkʌmftərbəl/",1150,14.3)
    elif k==3:
        word_title(d,T,"Vegetable",650,130,15.1,[(18.28,18.80),(WT[10][2][1],WT[10][2][2])])
        pillrow(d,L,880,False,"veg-e-ta-ble",T,16.88)
        pillrow(d,L,1030,True,None,T,18.28,syl=["VEJ","-tuh","-bul"],segs=[(18.28,18.80)])
        ipa(d,T,"/ˈvedʒtəbəl/",1150,18.35)
    else:
        for em,cx,t0 in ((emoji(("👥" if __import__("os").environ.get("FB") else "🔔"),230),400,0.05),(emoji("👍",230),680,0.35)):
            s=max(0.05,ease_out_back((lt-t0)/0.5)*(1+0.04*math.sin(T*6)));e=em.resize((int(em.width*s),int(em.height*s)),Image.LANCZOS);L.paste(e,(cx-e.width//2,360-e.height//2),e)
        a=clamp((lt-0.1)/0.3);sp=Image.new("RGBA",(W,700),(0,0,0,0));sd=ImageDraw.Draw(sp)
        sd.text((540,70),NAME,font=LA(150),fill=YEL,anchor="mm");ar(sd,(540,230),("تابع الصفحة" if __import__("os").environ.get("FB") else "اشترك في القناة"),96,CREAM,"ExtraBold");ar(sd,(540,345),"واعمل لايك",78,YEL,"Bold")
        pul=1+0.05*math.sin(T*7);bw,bh=int(520*pul),int(110*pul);sd.rounded_rectangle((540-bw//2,520-bh//2,540+bw//2,520+bh//2),bh//2,fill=CORAL);sd.text((540,520),("Follow" if __import__("os").environ.get("FB") else "Subscribe"),font=LA(58),fill=CREAM,anchor="mm")
        sp=fade(sp,a);L.paste(sp,(0,500),sp)
    return L
def main(out):
    BG=make_bg();SFXT=[(0.1,pop()),(1.2,pop()),(3.3,pop()),(WT[2][4][1],pop()),(6.24,pop()),(7.88,pop()),(10.9,pop()),(12.68,pop()),(14.24,pop()),(15.1,pop()),(16.88,pop()),(18.28,pop()),(19.25,pop()),(19.55,pop())]
    SFXT+=[(t,whoosh()) for t in (3.1,10.65,14.9,19.08)]
    mix(TOTAL,[(0.0,"/tmp/vo.wav")],SFXT,"/tmp/pron_all.wav")
    chip=Image.new("RGBA",(W,300),(0,0,0,0));cd=ImageDraw.Draw(chip);cd.rounded_rectangle((60,130,330,210),40,fill=YEL);ar(cd,(195,170),"نطق صح",44,NAVY)
    cd.rounded_rectangle((720,130,1000,210),40,fill=NAVY+(215,),outline=YEL+(255,),width=3);cd.text((860,170),NAME,font=LA(40),fill=CREAM,anchor="mm")
    def frame(T):
        im=bg_frame(BG,T).convert("RGBA");k=max(i for i,(a,b) in enumerate(SCN) if T>=a-1e-6)
        a,b=SCN[k];al=min(clamp((T-a)/0.25) if k>0 else 1,clamp((b-T)/0.2) if k<len(SCN)-1 else 1)
        lay=fade(scene_layer(T,k),al);im.paste(lay,(0,0),lay);im.paste(chip,(0,0),chip)
        caption(im,T);im=im.convert("RGB");progress(im,T,TOTAL);return im
    encode(TOTAL,frame,"/tmp/pron_all.wav",out)
if __name__=="__main__":main(sys.argv[1])
