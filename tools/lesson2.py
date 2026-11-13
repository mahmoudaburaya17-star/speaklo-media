"""Speaklo LESSON Reel v2: animated brand bg, pop/slide-in cards, karaoke word highlight synced to the voice, narrator + Sara/Adam, SFX + soft pad, safe zones, progress bar, loudnorm.
make(hook_ar(2 lines), hook_en, hook_voice, title_ar, sub_en, items, cta_lines, cta_voice, out)
items=[(keyword, meaning_ar, example_en, example_ar, emoji, (r,g,b), dark_text)]"""
import sys,os
sys.path.insert(0,'/home/claude/gen')
from fx import *
import voice
VO=["af_heart","am_adam"]
def wrap_words(d,text,font,maxw):
    words=text.split();lines=[[]];cur=""
    for w in words:
        n=(cur+" "+w).strip()
        if d.textlength(n,font=font)<=maxw or not lines[-1]:cur=n;lines[-1].append(w)
        else:lines.append([w]);cur=w
    return lines
def chip(d):d.rounded_rectangle((60,130,330,210),40,fill=YEL);ar(d,(195,170),"درس سريع",44,NAVY)
def fit(d,t,maxw,start=120):
    s=start
    while d.textlength(t,font=LA(s))>maxw and s>40:s-=4
    return LA(s)
def card_sprite(it):
    kw,mean,ex,exar,em,col,dark=it;tc=NAVY if dark else CREAM
    spr=Image.new("RGBA",(860,580),(0,0,0,0));d=ImageDraw.Draw(spr);d.rounded_rectangle((0,0,860,580),56,fill=col)
    d.text((430,380),kw,font=fit(d,kw,740),fill=tc,anchor="mm");ar(d,(430,500),mean,60,tc);return spr
def panel_sprite():
    spr=Image.new("RGBA",(920,430),(0,0,0,0));d=ImageDraw.Draw(spr);d.rounded_rectangle((0,40,920,430),48,fill=PANEL)
    d.rounded_rectangle((30,0,170,62),31,fill=YEL);ar(d,(100,31),"مثال",36,NAVY);return spr
def make(hook_ar,hook_en,hook_voice,title,sub,items,cta_lines,cta_voice,out,tmp="/tmp/lesson2"):
    os.makedirs(tmp,exist_ok=True);voices=[];sfx=[];ev=[];t=0.0
    du=voice.say(hook_voice,f"{tmp}/h.wav","bf_emma",0.9);voices.append((0.25,f"{tmp}/h.wav"));sfx.append((0.02,pop()))
    ev.append(dict(k="hook",s=t,e=t+du+0.85));t+=du+0.85
    scr=Image.new("RGB",(10,10));md=ImageDraw.Draw(scr);fe=LA(60)
    for i,it in enumerate(items):
        kd=voice.say(it[0],f"{tmp}/k{i}.wav","bf_emma",0.85);sd=voice.say(it[2],f"{tmp}/s{i}.wav",VO[i%2],0.9)
        ks=t+0.35;ss=ks+kd+0.3;sfx.append((t,whoosh()));sfx.append((t+0.22,pop()))
        voices+= [(ks,f"{tmp}/k{i}.wav"),(ss,f"{tmp}/s{i}.wav")]
        lines=wrap_words(md,it[2],fe,800);flat=[w for l in lines for w in l];wt=[len(w)+3 for w in flat];tot=sum(wt);acc=0;tm=[]
        for x in wt:tm.append((ss+sd*acc/tot,ss+sd*(acc+x)/tot));acc+=x
        ev.append(dict(k="item",s=t,e=ss+sd+0.75,it=it,i=i,lines=lines,tm=tm,ss=ss,sd=sd,card=card_sprite(it),em=emoji(it[4],240),keys=set(it[0].lower().split())));t=ss+sd+0.75
    cd=voice.say(cta_voice,f"{tmp}/c.wav","bf_emma",0.9);voices.append((t+0.5,f"{tmp}/c.wav"));sfx.append((t+0.1,pop()))
    ev.append(dict(k="cta",s=t,e=t+cd+1.3));t+=cd+1.3;total=t
    mix(total,voices,sfx,f"{tmp}/all.wav");BG=make_bg();pan=panel_sprite();hem=emoji("🤔",300);cem=emoji("👍",300)
    n=len(items)
    def frame(T):
        e=[x for x in ev if x["s"]<=T][-1];lt=T-e["s"];im=bg_frame(BG,T);d=ImageDraw.Draw(im);chip(d)
        if e["k"]=="hook":
            s=1+0.04*math.sin(T*5);em=hem.resize((int(hem.width*s),int(hem.height*s)),Image.LANCZOS);im.paste(em,(540-em.width//2,600-em.height//2),em)
            ar(d,(540,930),hook_ar[0],104,YEL,"ExtraBold");ar(d,(540,1070),hook_ar[1],104,CREAM,"ExtraBold");d.text((540,1240),hook_en,font=LA(54),fill=MINT,anchor="mm")
        elif e["k"]=="item":
            it=e["it"];ar(d,(540,300),title,72,YEL,"ExtraBold");d.text((540,375),sub,font=LA(36,"Medium"),fill=CREAM,anchor="mm")
            for j in range(n):
                cx=540+(j-(n-1)/2)*50;d.ellipse((cx-13,445-13,cx+13,445+13),fill=YEL if j==e["i"] else PANEL)
            a=clamp(lt/0.25);off=int((1-ease_out_back(lt/0.5))*320);cs=fade(e["card"],a);im.paste(cs,(110,520+off),cs)
            sc=ease_out_back((lt-0.15)/0.45);sz=max(8,int(e["em"].height*sc*(1+0.03*math.sin(T*3))));em=e["em"].resize((int(e["em"].width*sz/e["em"].height),sz),Image.LANCZOS)
            im.paste(em,(540-em.width//2,690+off-em.height//2),em)
            pa=clamp((lt-0.2)/0.3);ps=fade(pan,pa);im.paste(ps,(80,1120+int((1-pa)*40)),ps)
            if pa>0:
                y=1215;k=0
                for line in e["lines"]:
                    x=120
                    for w in line:
                        b,en=e["tm"][k];col=DIM if T<b else (YEL if T<en else CREAM);wd=d.textlength(w,font=fe)
                        d.text((x,y),w,font=fe,fill=col)
                        if w.strip(".,!?").lower() in e["keys"]:d.rounded_rectangle((x,y+68,x+wd,y+74),3,fill=it[5])
                        x+=wd+d.textlength(" ",font=fe);k+=1
                    y+=80
                aa=clamp((T-(e["ss"]+0.2))/0.4)
                if aa>0:
                    spr=Image.new("RGBA",(900,80),(0,0,0,0));ar(ImageDraw.Draw(spr),(450,40),it[3],50,YEL,"Medium");spr=fade(spr,aa);im.paste(spr,(90,y+30),spr)
        else:
            sc=ease_out_back(lt/0.5);s=max(0.05,sc*(1+0.05*math.sin(T*6)));em=cem.resize((int(cem.width*s),int(cem.height*s)),Image.LANCZOS);im.paste(em,(540-em.width//2,640-em.height//2),em)
            for q,(l,sz,col) in enumerate(zip(cta_lines,(78,58,58),(YEL,CREAM,CREAM))):ar(d,(540,960+q*115),l,sz,col,"ExtraBold" if q==0 else "Bold")
        progress(im,T,total);return im
    encode(total,frame,f"{tmp}/all.wav",out);return total
