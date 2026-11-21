"""Short 3: 3 ردود على Thank you غير You're welcome (No problem / Anytime / My pleasure)"""
from short_lib import *
VOICE="/tmp/vo3.wav";CHIP="قولها بالإنجليزي";TOTAL=24.0;SCN=[(0,5.0),(5.0,17.5),(17.5,24.0)];ROW_Y=(330,670,1010)
SEGS=[
 (0.24,1.54,prop(0.24,1.54,"لما حد يقولك Thank you"),True),
 (1.78,3.24,prop(1.78,3.24,"متردش بس You're welcome."),True),
 (3.76,4.70,prop(3.76,4.70,"فيه تلاتة ردود أحلى."),True),
 (5.38,6.00,prop(5.38,6.00,"أول واحد:"),True),
 (6.34,6.96,prop(6.34,6.96,"No problem."),False),
 (7.44,8.44,prop(7.44,8.44,"يعني ولا يهمك."),True),
 (9.14,9.56,prop(9.14,9.56,"التاني:"),True),
 (9.88,10.34,prop(9.88,10.34,"Anytime."),False),
 (10.76,11.68,prop(10.76,11.68,"يعني في أي وقت."),True),
 (12.32,12.76,prop(12.32,12.76,"والتالت،"),True),
 (13.12,14.44,prop(13.12,14.44,"ده للشغل والمواقف الشيك:"),True),
 (15.06,15.66,prop(15.06,15.66,"My pleasure."),False),
 (16.12,17.18,prop(16.12,17.18,"يعني من دواعي سروري."),True),
 (17.84,18.64,prop(17.84,18.64,"تابع Speaklo"),True),
 (19.00,21.76,prop(19.00,21.18,"وقولي في الكومنتات: بترد إزاي لما حد يقولك")+[("Sorry?",21.48,21.76)],True),
]
ROWS=[("No problem.","ولا يهمك",MINT,4,5.3,None),("Anytime.","في أي وقت",YEL,7,9.05,None),("My pleasure.","من دواعي سروري",CORAL,11,12.25,"للشغل والمواقف الشيك")]
def SFX():return [(0.1,pop()),(3.78,pop()),(5.3,pop()),(9.05,pop()),(12.25,pop()),(17.7,pop()),(18.0,pop())]+[(t,whoosh()) for t in (4.85,17.35)]
def hook(L,T,lt):
    s=ease_out_back(lt/0.5);em=emoji("🙏",300);e=em.resize((int(em.width*s)+1,int(em.height*s)+1),Image.LANCZOS);L.paste(e,(540-e.width//2,520-e.height//2),e)
    a=clamp((lt-0.2)/0.3);t=Image.new("RGBA",(W,420),(0,0,0,0));td=ImageDraw.Draw(t)
    f=LA(116);tw=f.getlength("Thank you");td.text((540-tw/2,100),"Thank you",font=f,fill=CREAM,anchor="ls")
    f2=LA(70);tw2=f2.getlength("You're welcome.");td.text((540-tw2/2,230),"You're welcome.",font=f2,fill=DIM,anchor="ls")
    t=fade(t,a);L.paste(t,(0,830),t)
    k=clamp((T-3.76)/0.5)
    if k>0:
        sp=Image.new("RGBA",(W,300),(0,0,0,0));sd=ImageDraw.Draw(sp);ar(sd,(540,110),"٣ ردود أحلى",120,YEL,"ExtraBold");sp=fade(sp,k)
        L.paste(sp,(0,1080-int(20*(1-ease_out_back(k)))),sp)
