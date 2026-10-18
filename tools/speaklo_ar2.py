from PIL import Image, ImageDraw, ImageFont, features
NAVY=(27,42,78);YEL=(255,201,60);CORAL=(255,107,74);MINT=(46,196,182);CREAM=(255,248,238)
S=2;W=1080*S
G="/home/claude/gen/";FD="/usr/share/fonts/truetype/google-fonts/"
def AR(sz,w="Bold"): return ImageFont.truetype(G+f"Tajawal-{w}.ttf",sz*S,layout_engine=ImageFont.Layout.RAQM)
def LA(sz,w="Bold"): return ImageFont.truetype(FD+f"Poppins-{w}.ttf",sz*S)
def new(bg): im=Image.new("RGB",(W,W),bg); return im,ImageDraw.Draw(im)
def tw(d,t,f,ar):
    kw=dict(direction="rtl",language="ar") if ar else {}
    b=d.textbbox((0,0),t,font=f,**kw); return b[2]-b[0],b[3]-b[1],b
def text(d,t,f,cx,y,fill,ar=True):
    w,h,b=tw(d,t,f,ar); kw=dict(direction="rtl",language="ar") if ar else {}
    d.text((cx*S-w/2-b[0],y*S-b[1]),t,font=f,fill=fill,**kw); return h/S
def wrap(d,t,f,maxw,ar=True):
    words=t.split();lines=[];cur=""
    for x in words:
        c=(cur+" "+x).strip()
        if tw(d,c,f,ar)[0]<=maxw*S or not cur: cur=c
        else: lines.append(cur);cur=x
    lines.append(cur);return lines
def block(d,t,f,cx,y,fill,maxw=900,ar=True,gap=14):
    for l in wrap(d,t,f,maxw,ar):
        h=text(d,l,f,cx,y,fill,ar);y+=h+gap
    return y
def chip(d,label,bg,fg,x=60,y=60):
    f=AR(34);w,h,_=tw(d,label,f,True);pw=w/S+56
    d.rounded_rectangle((x*S,y*S,(x+pw)*S,(y+66)*S),radius=33*S,fill=bg)
    text(d,label,f,x+pw/2,y+8,fg)
def logo(d,dark=True):
    c=YEL;d.rounded_rectangle((60*S,960*S,116*S,1016*S),radius=18*S,fill=c)
    text(d,"s",LA(36),88,964,NAVY,False)
    text(d,"Speaklo",LA(34),200,962,CREAM if dark else NAVY,False)
def save(im,out): im.resize((1080,1080),Image.LANCZOS).save(out)
def fit(d,t,maxsz,maxw,ar,fn):
    s=maxsz
    while s>20:
        f=fn(s)
        if max(tw(d,l,f,ar)[0] for l in t.split("\n"))<=maxw*S: return f
        s-=4
    return fn(20)
def word_ar(word,ipa,meaning,ex_en,ex_ar,out):
    im,d=new(NAVY);chip(d,"كلمة اليوم",YEL,NAVY)
    text(d,word.upper(),fit(d,word.upper(),150,900,False,lambda s:LA(s)),540,250,YEL,False)
    text(d,ipa,ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",44*S),540,450,CREAM,False)
    text(d,meaning,AR(78),540,560,CREAM)
    d.rounded_rectangle((90*S,720*S,990*S,920*S),radius=36*S,fill=(40,58,100))
    y=block(d,ex_en,LA(36,"Medium"),540,745,CREAM,780,False,10)
    block(d,ex_ar,AR(34,"Medium"),540,y+4,YEL,780)
    logo(d);save(im,out)
def mistake_ar(wrong,right,note,out):
    im,d=new(CREAM);chip(d,"غلطة شائعة",NAVY,CREAM)
    d.rounded_rectangle((60*S,170*S,1020*S,470*S),radius=40*S,fill=CORAL)
    d.rounded_rectangle((60*S,490*S,1020*S,790*S),radius=40*S,fill=MINT)
    for lab,t,y0,col in(("غلط ✗",wrong,170,CORAL),("صح ✓",right,490,MINT)):
        text(d,lab.split()[0],AR(40),540,y0+22,CREAM)
        f=fit(d,t,56,840,False,lambda s:LA(s));lines=wrap(d,t,f,840,False)
        y=y0+95 if len(lines)<3 else y0+85
        for l in lines: y+=text(d,l,f,540,y,CREAM,False)+10
    block(d,note,AR(36,"Medium"),540,815,NAVY,900,True,8)
    logo(d,False);save(im,out)
def quiz_ar(q,opts,out):
    im,d=new(NAVY);chip(d,"كويز",CORAL,CREAM)
    f=fit(d,q,72,900,False,lambda s:LA(s));y=block(d,q,f,540,230,YEL,900,False,16)
    y=max(y+40,420)
    for i,o in enumerate(opts):
        yy=y+i*150
        d.rounded_rectangle((120*S,yy*S,960*S,(yy+120)*S),radius=60*S,fill=CORAL)
        text(d,"ABC"[i]+")  "+o,LA(48),540,yy+30,CREAM,False)
    text(d,"اكتب إجابتك في الكومنتات",AR(40,"Medium"),540,880,CREAM)
    logo(d);save(im,out)
def title_ar(chipl,title,sub,out):
    im,d=new(NAVY);chip(d,chipl,YEL,NAVY)
    f=AR(40,"ExtraBold")
    for sz in range(150,40,-6):
        f=AR(sz,"ExtraBold")
        if len(wrap(d,title,f,880,True))<=3: break
    y=block(d,title,f,540,260,YEL,880,True,24)
    block(d,sub,AR(46,"Medium"),540,y+50,CREAM,860)
    logo(d);save(im,out)
