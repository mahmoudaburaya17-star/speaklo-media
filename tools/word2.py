"""Speaklo WORD Reel v2 (fx kit): Arabic hook, animated bg, word card pop-in, word said twice, example with karaoke, light CTA.
make(chip_ar, hook_ar(2 lines), hook_voice, word, ipa, meaning_ar, ex_en, ex_ar, emoji_ch, col, dark, cta_lines, cta_voice, out)"""
import sys,os
sys.path.insert(0,'/home/claude/gen')
from fx import *
import voice
from lesson2 import wrap_words,fit,panel_sprite
def make(chip_ar,hook_ar,hook_voice,word,ipa,mean,ex,exar,em_ch,col,dark,cta_lines,cta_voice,out,tmp="/tmp/word2"):
    os.makedirs(tmp,exist_ok=True);voices=[];sfx=[];ev=[];t=0.0;tc=NAVY if dark else CREAM
    hd=voice.say(hook_voice,f"{tmp}/h.wav","bf_emma",0.9);voices.append((0.25,f"{tmp}/h.wav"));sfx.append((0.02,pop()))
    ev.append(dict(k="hook",s=t,e=t+hd+0.8));t+=hd+0.8
    w1=voice.say(word,f"{tmp}/w1.wav","bf_emma",0.85);w2=voice.say(word,f"{tmp}/w2.wav","bf_emma",0.65);sd=voice.say(ex,f"{tmp}/e.wav","af_heart",0.9)
    sfx.append((t,whoosh()));sfx.append((t+0.22,pop()));a=t+0.4;voices.append((a,f"{tmp}/w1.wav"));b=a+w1+0.45;voices.append((b,f"{tmp}/w2.wav"));ss=b+w2+0.5;voices.append((ss,f"{tmp}/e.wav"))
    scr=Image.new("RGB",(10,10));md=ImageDraw.Draw(scr);fe=LA(60);lines=wrap_words(md,ex,fe,800);flat=[w for l in lines for w in l];wt=[len(w)+3 for w in flat];tot=sum(wt);acc=0;tm=[]
    for x in wt:tm.append((ss+sd*acc/tot,ss+sd*(acc+x)/tot));acc+=x
    ev.append(dict(k="word",s=t,e=ss+sd+0.8,ss=ss,tm=tm,lines=lines,w1=a,w2=b));t=ss+sd+0.8
    cd=voice.say(cta_voice,f"{tmp}/c.wav","bf_emma",0.9);voices.append((t+0.5,f"{tmp}/c.wav"));sfx.append((t+0.1,pop()));ev.append(dict(k="cta",s=t,e=t+cd+1.3));t+=cd+1.3;total=t
    mix(total,voices,sfx,f"{tmp}/all.wav");BG=make_bg();pan=panel_sprite();hem=emoji("✨",280);wem=emoji(em_ch,230);cem=emoji("👍",300)
    card=Image.new("RGBA",(860,600),(0,0,0,0));cd_=ImageDraw.Draw(card);cd_.rounded_rectangle((0,0,860,600),56,fill=col)
    cd_.text((430,385),word.upper(),font=fit(cd_,word.upper(),740,130),fill=tc,anchor="mm");cd_.text((430,470),ipa,font=__import__("PIL.ImageFont",fromlist=["x"]).truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",46),fill=tc,anchor="mm");ar(cd_,(430,545),mean,64,tc)
    def chip(d):d.rounded_rectangle((60,130,340,210),40,fill=YEL);ar(d,(200,170),chip_ar,44,NAVY)
    def frame(T):
        e=[x for x in ev if x["s"]<=T][-1];lt=T-e["s"];im=bg_frame(BG,T);d=ImageDraw.Draw(im);chip(d)
        if e["k"]=="hook":
            s=1+0.04*math.sin(T*5);em=hem.resize((int(hem.width*s),int(hem.height*s)),Image.LANCZOS);im.paste(em,(540-em.width//2,640-em.height//2),em)
            ar(d,(540,960),hook_ar[0],100,YEL,"ExtraBold");ar(d,(540,1100),hook_ar[1],100,CREAM,"ExtraBold")
        elif e["k"]=="word":
            a=clamp(lt/0.25);off=int((1-ease_out_back(lt/0.5))*320);cs=fade(card,a);im.paste(cs,(110,300+off),cs)
            sc=ease_out_back((lt-0.15)/0.45);sz=max(8,int(wem.height*sc*(1+0.03*math.sin(T*3))));em=wem.resize((int(wem.width*sz/wem.height),sz),Image.LANCZOS);im.paste(em,(540-em.width//2,440+off-em.height//2),em)
            pa=clamp((lt-0.5)/0.3);ps=fade(pan,pa);im.paste(ps,(80,980+int((1-pa)*40)),ps)
            if pa>0:
                y=1075;k=0
                for line in e["lines"]:
                    x=120
                    for w in line:
                        b,en=e["tm"][k];col_=DIM if T<b else (YEL if T<en else CREAM);d.text((x,y),w,font=fe,fill=col_);x+=d.textlength(w,font=fe)+d.textlength(" ",font=fe);k+=1
                    y+=80
                aa=clamp((T-(e["ss"]+0.2))/0.4)
                if aa>0:
                    spr=Image.new("RGBA",(900,80),(0,0,0,0));ar(ImageDraw.Draw(spr),(450,40),exar,50,YEL,"Medium");spr=fade(spr,aa);im.paste(spr,(90,y+30),spr)
        else:
            sc=ease_out_back(lt/0.5);s=max(0.05,sc*(1+0.05*math.sin(T*6)));em=cem.resize((int(cem.width*s),int(cem.height*s)),Image.LANCZOS);im.paste(em,(540-em.width//2,640-em.height//2),em)
            for q,(l,sz,c) in enumerate(zip(cta_lines,(78,58,58),(YEL,CREAM,CREAM))):ar(d,(540,960+q*115),l,sz,c,"ExtraBold" if q==0 else "Bold")
        progress(im,T,total);return im
    encode(total,frame,f"{tmp}/all.wav",out);return total
