"""Short 2: 'أنا مش فاضي دلوقتي' بالإنجليزي الصح (I'm not free right now / I'm swamped / I'm tied up at the moment)"""
from short_lib import *
VOICE="/tmp/vo2.wav";CHIP="قولها بالإنجليزي";TOTAL=19.5;SCN=[(0,3.99),(3.99,12.2),(12.2,19.5)];ROW_Y=(330,670,1010)
SEGS=[
 (0.26,1.26,prop(0.26,1.26,"متقولش I'm not empty!"),True),
 (1.62,3.82,prop(1.62,3.82,"«أنا مش فاضي دلوقتي» بالإنجليزي الصح هي:"),True),
 (4.16,5.34,prop(4.16,5.34,"I'm not free right now."),False),
 (5.90,7.50,prop(5.90,7.50,"ولو مشغول جدا، ممكن تقول:"),True),
 (7.78,8.52,prop(7.78,8.52,"I'm swamped."),False),
 (9.00,10.38,[("وفي",9.00,9.25),("الشغل،",9.25,9.60),("بأدب",9.72,10.05),("كده:",10.05,10.38)],True),
 (10.72,11.82,prop(10.72,11.82,"I'm tied up at the moment."),False),
 (12.60,14.66,prop(12.60,14.66,"تابع Speaklo عشان كل يوم جملة جديدة،"),True),
 (14.94,16.92,prop(14.94,16.92,"واكتب في الكومنتات جملة عايز تقولها بالإنجليزي."),True),
]
ROWS=[("I'm not free right now.","أنا مش فاضي دلوقتي",MINT,2,4.0,None),("I'm swamped.","مشغول جدًا",YEL,4,7.6,None),("I'm tied up at the moment.","بأدب في الشغل",CORAL,6,10.6,None)]
def SFX():return [(0.1,pop()),(1.0,pop()),(4.0,pop()),(7.6,pop()),(10.6,pop()),(12.3,pop()),(12.6,pop())]+[(t,whoosh()) for t in (3.85,12.0)]
def hook(L,T,lt):
    s=ease_out_back(lt/0.5);em=emoji("🙅",300);e=em.resize((int(em.width*s)+1,int(em.height*s)+1),Image.LANCZOS);L.paste(e,(540-e.width//2,560-e.height//2),e)
    a=clamp((lt-0.3)/0.3);t=Image.new("RGBA",(W,200),(0,0,0,0));td=ImageDraw.Draw(t);f=LA(104);txt="I'm not empty!";tw=f.getlength(txt)
    td.text((540-tw/2,110),txt,font=f,fill=CORAL,anchor="ls");k2=clamp((T-1.0)/0.4)
    if k2>0:td.line((540-tw/2-10,70,540-tw/2-10+(tw+20)*k2,70),fill=CREAM,width=10)
    t=fade(t,a);L.paste(t,(0,860),t)
    if T>=1.3:
        s=ease_out_back((T-1.3)/0.4);em=emoji("❌",180);e=em.resize((int(em.width*s)+1,int(em.height*s)+1),Image.LANCZOS);L.paste(e,(540-e.width//2,1130-e.height//2),e)
