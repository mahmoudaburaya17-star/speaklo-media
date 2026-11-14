"""Speaklo DIALOGUE Reel v2 (fx kit): Arabic hook, animated bg, avatars pulse, stacked chat bubbles sliding in, karaoke on the spoken bubble, SFX, light CTA.
make(title_ar, sub_en, hook_ar(2 lines), hook_voice, lines[(sp,en,ar)], cta_lines, cta_voice, out)"""
import sys,os
sys.path.insert(0,'/home/claude/gen')
from fx import *
import voice
from lesson2 import wrap_words
VO={0:"af_heart",1:"am_adam"};NM={0:"Sara",1:"Adam"};BC={0:CORAL,1:MINT}
PAL={0:dict(spoken=CREAM,cur=NAVY,up=(255,196,176),ar=CREAM),1:dict(spoken=NAVY,cur=(255,255,255),up=(30,120,115),ar=NAVY)}
BW,BH=860,236
def make(title,sub,hook_ar,hook_voice,lines,cta_lines,cta_voice,out,tmp="/tmp/dialogue2"):
    os.makedirs(tmp,exist_ok=True);voices=[];sfx=[];t=0.0;ev=[]
    hd=voice.say(hook_voice,f"{tmp}/h.wav","bf_emma",0.9);voices.append((0.25,f"{tmp}/h.wav"));sfx.append((0.02,pop()));ev.append(dict(k="hook",s=t,e=t+hd+0.8));t+=hd+0.8
    scr=Image.new("RGB",(10,10));md=ImageDraw.Draw(scr);fe=LA(44);B=[]
    for i,(sp,en,arx) in enumerate(lines):
        du=voice.say(en,f"{tmp}/l{i}.wav",VO[sp],0.9);voices.append((t+0.35,f"{tmp}/l{i}.wav"));sfx.append((t,pop()))
        wl=wrap_words(md,en,fe,760);flat=[w for l in wl for w in l];wt=[len(w)+3 for w in flat];tot=sum(wt);acc=0;tm=[];ss=t+0.35
        for x in wt:tm.append((ss+du*acc/tot,ss+du*(acc+x)/tot));acc+=x
        B.append(dict(sp=sp,en=en,ar=arx,wl=wl,tm=tm));ev.append(dict(k="line",s=t,e=ss+du+0.6,i=i));t=ss+du+0.6
    cd=voice.say(cta_voice,f"{tmp}/c.wav","bf_emma",0.9);voices.append((t+0.5,f"{tmp}/c.wav"));sfx.append((t+0.1,pop()));ev.append(dict(k="cta",s=t,e=t+cd+1.3));t+=cd+1.3;total=t
    mix(total,voices,sfx,f"{tmp}/all.wav");BG=make_bg();hem=emoji("💬",280);cem=emoji("👍",300)
    def bubble(b,T,active):
        spr=Image.new("RGBA",(BW,BH),(0,0,0,0));d=ImageDraw.Draw(spr);p=PAL[b["sp"]];d.rounded_rectangle((0,0,BW,BH),44,fill=BC[b["sp"]]);k=0;y=28
        d.text((34,18),NM[b["sp"]],font=LA(26,"Medium"),fill=p["up"] if b["sp"]==0 else p["up"]);y=58
        for line in b["wl"]:
            x=50
            for w in line:
                st,en=b["tm"][k];c=p["spoken"] if not active else (p["up"] if T<st else (p["cur"] if T<en else p["spoken"]))
                d.text((x,y),w,font=fe,fill=c);x+=d.textlength(w,font=fe)+d.textlength(" ",font=fe);k+=1
            y+=56
        ar(d,(BW//2,BH-38),b["ar"],40,p["ar"],"Medium");return spr
    def chip(d):d.rounded_rectangle((60,130,330,210),40,fill=YEL);ar(d,(195,170),"محادثة",44,NAVY)
    def frame(T):
        e=[x for x in ev if x["s"]<=T][-1];lt=T-e["s"];im=bg_frame(BG,T);d=ImageDraw.Draw(im);chip(d)
        if e["k"]=="hook":
            s=1+0.04*math.sin(T*5);em=hem.resize((int(hem.width*s),int(hem.height*s)),Image.LANCZOS);im.paste(em,(540-em.width//2,640-em.height//2),em)
            ar(d,(540,960),hook_ar[0],100,YEL,"ExtraBold");ar(d,(540,1100),hook_ar[1],100,CREAM,"ExtraBold");d.text((540,1260),sub,font=LA(50),fill=MINT,anchor="mm")
        elif e["k"]=="line":
            a=e["i"];ar(d,(540,300),title,72,YEL,"ExtraBold");d.text((540,375),sub,font=LA(36,"Medium"),fill=CREAM,anchor="mm")
            act=B[a]["sp"]
            for sp,cx in ((0,300),(1,780)):
                r=62*(1+(0.07*math.sin(T*14) if act==sp else 0));cy=520
                if act==sp:d.ellipse((cx-r-10,cy-r-10,cx+r+10,cy+r+10),outline=YEL,width=6)
                d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=BC[sp]);d.text((cx,cy),NM[sp][0],font=LA(64),fill=NAVY if sp==1 else CREAM,anchor="mm");d.text((cx,cy+92),NM[sp],font=LA(28),fill=CREAM,anchor="mm")
            ease=ease_out_cubic(lt/0.35)
            for k in range(max(0,a-2),a+1):
                slot=2-(a-k)+(1-ease)*(1 if k<a else 0);y=700+int(slot*(BH+24))+(int((1-ease)*100) if k==a else 0)
                spr=bubble(B[k],T,k==a);al=1.0 if k==a else (0.55 if True else 1)
                if k==a:al=clamp(lt/0.2)
                spr=fade(spr,al);x=80 if B[k]["sp"]==0 else 140;im.paste(spr,(x,y),spr)
        else:
            sc=ease_out_back(lt/0.5);s=max(0.05,sc*(1+0.05*math.sin(T*6)));em=cem.resize((int(cem.width*s),int(cem.height*s)),Image.LANCZOS);im.paste(em,(540-em.width//2,640-em.height//2),em)
            for q,(l,sz,c) in enumerate(zip(cta_lines,(78,58,58),(YEL,CREAM,CREAM))):ar(d,(540,960+q*115),l,sz,c,"ExtraBold" if q==0 else "Bold")
        progress(im,T,total);return im
    encode(total,frame,f"{tmp}/all.wav",out);return total
