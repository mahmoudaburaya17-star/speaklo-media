import sys,os;sys.path.insert(0,'/home/claude/gen')
import speaklo_ar2 as M
from speaklo_ar2 import NAVY,YEL,CREAM,AR,LA,new
from PIL import Image,ImageFont
K=M.S;Wd=1080*K;Hd=1920*K
DJ=lambda n:ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",n*K)
def canvas():
    im=Image.new("RGB",(Wd,Hd),NAVY);d=M.ImageDraw.Draw(im);M.chip(d,"كلمة اليوم",YEL,NAVY,x=60,y=120)
    d.rounded_rectangle((60*K,1700*K,116*K,1756*K),radius=18*K,fill=YEL);M.text(d,"s",LA(36),88,1704,NAVY,False);M.text(d,"Speaklo",LA(34),200,1702,CREAM,False);return im,d
def fin(im,p): im.resize((1080,1920),Image.LANCZOS).save(p)
word,ipa,ar,ex,exar="prefer","/prɪˈfɜːr/","يفضّل","I prefer tea to coffee.","أفضّل الشاي على القهوة."
out="/home/claude/gen/reelf";os.makedirs(out,exist_ok=True)
im,d=canvas();M.text(d,word.upper(),M.fit(d,word.upper(),170,920,False,lambda s:LA(s)),540,760,YEL,False);fin(im,out+"/s1.png")
im,d=canvas();M.text(d,word.upper(),LA(110),540,560,YEL,False);M.text(d,ipa,DJ(56),540,780,CREAM,False);M.text(d,ar,AR(130),540,960,CREAM);fin(im,out+"/s2.png")
im,d=canvas();M.text(d,word.upper(),LA(110),540,360,YEL,False)
d.rounded_rectangle((70*K,640*K,1010*K,1140*K),radius=50*K,fill=(40,58,100))
y=M.block(d,ex,LA(58,"Medium"),540,720,CREAM,820,False,18);M.block(d,exar,AR(52,"Medium"),540,y+30,YEL,820);fin(im,out+"/s3.png")
im,d=canvas();M.text(d,word.upper(),LA(110),540,500,YEL,False);M.block(d,"اكتب جملتك بالكلمة دي في الكومنتات",AR(72),540,800,CREAM,860);M.text(d,"تابع Speaklo",AR(56,"Medium"),540,1250,YEL);fin(im,out+"/s4.png")
