"""Speaklo STORY Reel v2 (fx kit): Arabic hook, animated bg, pop-in scene card with slow zoom, karaoke highlight on the spoken English sentence, narrator + Sara + Adam, SFX + pad, word cards, light CTA, loudnorm, safe zones.
make(title_ar, sub_en, hook_ar(2 lines), hook_voice, scenes, words, cta_lines, cta_voice, out)
scenes=[(speaker 'N'|0|1, english, arabic, emoji, (r,g,b), dark_text)]; words=[(EN, AR)]"""
import sys,os,math
sys.path.insert(0,'/home/claude/gen')
from fx import *
import voice
from lesson2 import wrap_words
VOICES={"N":"bf_emma",0:"af_heart",1:"am_adam"};NAMES={"N":"Narrator",0:"Sara",1:"Adam"};CHC={"N":YEL,0:CORAL,1:MINT}
def panel():
    spr=Image.new("RGBA",(920,560),(0,0,0,0));ImageDraw.Draw(spr).rounded_rectangle((0,40,920,560),48,fill=PANEL);return spr
def make(title,sub,hook_ar,hook_voice,scenes,words,cta_lines,cta_voice,out,tmp="/tmp/story2"):
    os.makedirs(tmp,exist_ok=True);voices=[];sfx=[];ev=[];t=0.0
    hd=voice.say(hook_voice,f"{tmp}/h.wav","bf_emma",0.9);voices.append((0.25,f"{tmp}/h.wav"));sfx.append((0.02,pop()));ev.append(dict(k="hook",s=t,e=t+hd+0.8));t+=hd+0.8
    scr=Image.new("RGB",(10,10));md=ImageDraw.Draw(scr);fe=LA(52)
    for i,(sp,en,arx,em,col,dark) in enumerate(scenes):
        du=voice.say(en,f"{tmp}/l{i}.wav",VOICES[sp],0.9);ss=t+0.4;voices.append((ss,f"{tmp}/l{i}.wav"));sfx.append((t,whoosh() if i==0 or scenes[i-1][0]!=sp else pop()));sfx.append((t+0.2,pop()))
        lines=wrap_words(md,en,fe,800);flat=[w for l in lines for w in l];wt=[len(w)+3 for w in flat];tot=sum(wt);acc=0;tm=[]
        for x in wt:tm.append((ss+du*acc/tot,ss+du*(acc+x)/tot));acc+=x
        ev.append(dict(k="scene",s=t,e=ss+du+0.55,i=i,sc=scenes[i],lines=lines,tm=tm,ss=ss,du=du,em=emoji(em,330)));t=ss+du+0.55
    for i,(en,arx) in enumerate(words):
        d1=voice.say(en,f"{tmp}/w{i}.wav","bf_emma",0.85);sfx.append((t,pop()));voices.append((t+0.2,f"{tmp}/w{i}.wav"));ev.append(dict(k="words",s=t,e=t+d1+0.9,n=i));t+=d1+0.9
    cd=voice.say(cta_voice,f"{tmp}/c.wav","bf_emma",0.9);voices.append((t+0.5,f"{tmp}/c.wav"));sfx.append((t+0.1,pop()));ev.append(dict(k="cta",s=t,e=t+cd+1.3));t+=cd+1.3;total=t
    mix(total,voices,sfx,f"{tmp}/all.wav");BG=make_bg();pan=panel();hem=emoji("📖",300);cem=emoji("👍",300);N=len(scenes)
    def frame(T):
        e=[x for x in ev if x["s"]<=T][-1];lt=T-e["s"];im=bg_frame(BG,T);d=ImageDraw.Draw(im)
        d.rounded_rectangle((60,130,330,210),40,fill=YEL);ar(d,(195,170),"قصة",44,NAVY)
        if e["k"]=="hook":
            s=1+0.04*math.sin(T*5);em=hem.resize((int(hem.width*s),int(hem.height*s)),Image.LANCZOS);im.paste(em,(540-em.width//2,640-em.height//2),em)
            ar(d,(540,960),hook_ar[0],100,YEL,"ExtraBold");ar(d,(540,1100),hook_ar[1],100,CREAM,"ExtraBold")
        elif e["k"]=="scene":
            sp,en,arx,emj,col,dark=e["sc"];tc=NAVY if dark else CREAM
            ar(d,(540,300),title,72,YEL,"ExtraBold");d.text((540,375),sub,font=LA(36,"Medium"),fill=CREAM,anchor="mm")
            for j in range(N):
                cx=540+(j-(N-1)/2)*34;d.ellipse((cx-9,440-9,cx+9,440+9),fill=YEL if j==e["i"] else PANEL)
            a=clamp(lt/0.25);off=int((1-ease_out_back(lt/0.5))*300)
            card=Image.new("RGBA",(860,500),(0,0,0,0));ImageDraw.Draw(card).rounded_rectangle((0,0,860,500),56,fill=col);cs=fade(card,a);im.paste(cs,(110,490+off),cs)
            sc=ease_out_back((lt-0.1)/0.45);zoom=1+0.03*lt;sz=max(8,int(e["em"].height*sc*zoom));em=e["em"].resize((int(e["em"].width*sz/e["em"].height),sz),Image.LANCZOS);im.paste(em,(540-em.width//2,740+off-em.height//2),em)
            pa=clamp((lt-0.2)/0.3);ps=fade(pan,pa);im.paste(ps,(80,1020+int((1-pa)*40)),ps)
            if pa>0:
                lab=NAMES[sp];c=CHC[sp];w_=int(d.textlength(lab,font=LA(34)))+50;d.rounded_rectangle((120,1000,120+w_,1062),31,fill=c);d.text((145,1031),lab,font=LA(34),fill=NAVY if sp!=0 else CREAM,anchor="lm")
                y=1110;k=0
                for line in e["lines"]:
                    x=120
                    for w in line:
                        b,en_=e["tm"][k];cc=DIM if T<b else (YEL if T<en_ else CREAM);d.text((x,y),w,font=fe,fill=cc);x+=d.textlength(w,font=fe)+d.textlength(" ",font=fe);k+=1
                    y+=68
                aa=clamp((T-(e["ss"]+0.2))/0.4)
                if aa>0:
                    spr=Image.new("RGBA",(900,80),(0,0,0,0));ar(ImageDraw.Draw(spr),(450,40),arx,44,YEL,"Medium");spr=fade(spr,aa);im.paste(spr,(90,y+14),spr)
        elif e["k"]=="words":
            ar(d,(540,330),"كلمات القصة",84,YEL,"ExtraBold");d.text((540,415),"New words",font=LA(40,"Medium"),fill=CREAM,anchor="mm")
            for i,(wen,war) in enumerate(words):
                if i>e["n"]:break
                l2=lt if i==e["n"] else 9;off=int((1-ease_out_back(l2/0.45))*260);y=520+i*290
                spr=Image.new("RGBA",(860,250),(0,0,0,0));sd=ImageDraw.Draw(spr);cc=[CORAL,MINT,YEL][i%3];tcc=CREAM if i%3==0 else NAVY
                sd.rounded_rectangle((0,0,860,250),50,fill=cc);sd.text((430,95),wen.upper(),font=LA(86),fill=tcc,anchor="mm");ar(sd,(430,190),war,60,tcc)
                spr=fade(spr,clamp(l2/0.2));im.paste(spr,(110,y+off),spr)
        else:
            sc=ease_out_back(lt/0.5);s=max(0.05,sc*(1+0.05*math.sin(T*6)));em=cem.resize((int(cem.width*s),int(cem.height*s)),Image.LANCZOS);im.paste(em,(540-em.width//2,640-em.height//2),em)
            for q,(l,sz,cc) in enumerate(zip(cta_lines,(78,58,58),(YEL,CREAM,CREAM))):ar(d,(540,960+q*115),l,sz,cc,"ExtraBold" if q==0 else "Bold")
        progress(im,T,total);return im
    encode(total,frame,f"{tmp}/all.wav",out);return total
