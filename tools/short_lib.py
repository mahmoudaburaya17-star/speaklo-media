"""Generic Speaklo 'phrase Short' renderer for a user voiceover (hook -> cards that stack up -> CTA).
A config module (see cfg_notfree.py / cfg_thanks.py) provides: VOICE, CHIP, SEGS, ROWS, SCN, TOTAL, SFX, hook(L,T,lt).
SEGS=[(start,end,[(word,s,e)],captioned)]  measured from the voiceover; ROWS=[(english,arabic,color,seg_index,appear_time,tag)]
usage: python short_lib.py cfg_module out.mp4"""
import sys,math,importlib
sys.path.insert(0,'/home/claude/gen')
from fx import *
NAME="Speaklo"
def prop(a,b,text):
    ws=text.split();wt=[len(w)+1.5 for w in ws];tot=sum(wt);acc=0;out=[]
    for w,x in zip(ws,wt):out.append((w,a+(b-a)*acc/tot,a+(b-a)*(acc+x)/tot));acc+=x
    return out
def isar(w):return any("؀"<=c<="ۿ" for c in w)
def wfont(w,s):return AR(s,"Bold") if isar(w) else LA(s)
def tlen(parts,s):
    """parts=[(word,s,e)] of one token; arabic token has one part, latin token may have many (LTR run)"""
    w0=parts[0][0]
    if isar(w0):f=wfont(w0,s);return f.getlength(w0,direction="rtl",language="ar")
    f=LA(s);return f.getlength(" ".join(p[0] for p in parts))
def tokens(ws):
    out=[]
    for w,s,e in ws:
        if out and not isar(w) and not isar(out[-1][0][0]):out[-1].append((w,s,e))
        else:out.append([(w,s,e)])
    return out
def draw_token(d,cx,y,parts,T,size):
    def col(s,e):return YEL if s<=T<e else (CREAM if T>=e else DIM)
    w0=parts[0][0]
    if isar(w0):d.text((cx,y),w0,font=wfont(w0,size),fill=col(parts[0][1],parts[0][2]),anchor="mm",direction="rtl",language="ar");return
    f=LA(size);tot=tlen(parts,size);x=cx-tot/2
    for i,(w,s,e) in enumerate(parts):
        t=w+(" " if i<len(parts)-1 else "");d.text((x,y),t,font=f,fill=col(s,e),anchor="lm");x+=f.getlength(t)
def caption(C,im,T):
    cur=None
    for a,b,ws,cap in C.SEGS:
        if cap and a-0.05<=T<=b+0.35:cur=(a,b,ws)
    if not cur:return
    a,b,ws=cur;al=min(clamp((T-(a-0.05))/0.12),clamp((b+0.35-T)/0.15))
    size=64;maxw=860;lines=[[]];cw=0
    for tk in tokens(ws):
        L=tlen(tk,size)+22
        if cw+L>maxw and lines[-1]:lines.append([]);cw=0
        lines[-1].append((tk,L));cw+=L
    ov=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(ov)
    ph=len(lines)*104+60;y0=1410-ph//2
    d.rounded_rectangle((70,y0,1010,y0+ph),44,fill=PANEL+(215,),outline=DIM+(90,),width=2)
    for li,ln in enumerate(lines):
        tw=sum(L for _,L in ln)-22;x=540+tw/2;y=y0+30+52+li*104
        for tk,L in ln:
            draw_token(d,x-(L-22)/2,y,tk,T,size);x-=L
    ov=fade(ov,al);im.paste(ov,(0,0),ov)
def row(C,L,T,idx,y):
    txt,arb,col,si,t0,tag=C.ROWS[idx];ws=C.SEGS[si][2];k=clamp((T-t0)/0.4)
    if k<=0:return
    s=ease_out_back(k);sp=Image.new("RGBA",(W,310),(0,0,0,0));d=ImageDraw.Draw(sp)
    d.rounded_rectangle((90,10,990,290),38,fill=PANEL+(235,));d.rounded_rectangle((90,10,114,290),12,fill=col)
    f=LA(64);tw=sum(f.getlength(w+" ") for w,_,_ in ws)-f.getlength(" ");x=540-tw/2+12
    for w,ws_,we in ws:
        t=w+" ";c=YEL if ws_<=T<we else CREAM;d.text((x,110),t,font=f,fill=c,anchor="lm");x+=f.getlength(t)
    ar(d,(540,224),arb,56,col,"Bold")
    if tag:
        tw2=AR(34,"Bold").getlength(tag,direction="rtl",language="ar")+44;d.rounded_rectangle((990-tw2-20,24,990-20,74),25,fill=col);ar(d,(990-20-tw2/2,49),tag,32,NAVY,"Bold")
    sp=fade(sp,k);L.paste(sp,(0,int(y+(1-s)*40)-10),sp)
def scene_layer(C,T,k):
    L=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(L);lt=T-C.SCN[k][0]
    if k==0:C.hook(L,T,lt)
    elif k==1:
        for i,y in enumerate(C.ROW_Y[:len(C.ROWS)]):row(C,L,T,i,y)
    else:
        for em,cx,t0 in ((emoji("🔔",230),400,0.05),(emoji("👍",230),680,0.35)):
            s=max(0.05,ease_out_back((lt-t0)/0.5)*(1+0.04*math.sin(T*6)));e=em.resize((int(em.width*s),int(em.height*s)),Image.LANCZOS);L.paste(e,(cx-e.width//2,360-e.height//2),e)
        a=clamp((lt-0.1)/0.3);sp=Image.new("RGBA",(W,700),(0,0,0,0));sd=ImageDraw.Draw(sp)
        sd.text((540,70),NAME,font=LA(150),fill=YEL,anchor="mm");ar(sd,(540,230),"اشترك في القناة",96,CREAM,"ExtraBold");ar(sd,(540,345),"واعمل لايك",78,YEL,"Bold")
        pul=1+0.05*math.sin(T*7);bw,bh=int(520*pul),int(110*pul);sd.rounded_rectangle((540-bw//2,520-bh//2,540+bw//2,520+bh//2),bh//2,fill=CORAL);sd.text((540,520),"Subscribe",font=LA(58),fill=CREAM,anchor="mm")
        sp=fade(sp,a);L.paste(sp,(0,500),sp)
    return L
def main(cfg,out):
    C=importlib.import_module(cfg);BG=make_bg()
    mix(C.TOTAL,[(0.0,C.VOICE)],C.SFX(),"/tmp/short_all.wav")
    chip=Image.new("RGBA",(W,300),(0,0,0,0));cd=ImageDraw.Draw(chip);cw=AR(44,"Bold").getlength(C.CHIP,direction="rtl",language="ar")+80
    cd.rounded_rectangle((60,130,60+cw,210),40,fill=YEL);ar(cd,(60+cw/2,170),C.CHIP,44,NAVY)
    cd.rounded_rectangle((720,130,1000,210),40,fill=NAVY+(215,),outline=YEL+(255,),width=3);cd.text((860,170),NAME,font=LA(40),fill=CREAM,anchor="mm")
    def frame(T):
        im=bg_frame(BG,T).convert("RGBA");k=max(i for i,(a,b) in enumerate(C.SCN) if T>=a-1e-6)
        a,b=C.SCN[k];al=min(clamp((T-a)/0.25) if k>0 else 1,clamp((b-T)/0.2) if k<len(C.SCN)-1 else 1)
        lay=fade(scene_layer(C,T,k),al);im.paste(lay,(0,0),lay);im.paste(chip,(0,0),chip)
        caption(C,im,T);im=im.convert("RGB");progress(im,T,C.TOTAL);return im
    encode(C.TOTAL,frame,"/tmp/short_all.wav",out)
if __name__=="__main__":main(sys.argv[1],sys.argv[2])
