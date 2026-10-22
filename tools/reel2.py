import sys,os,subprocess;sys.path.insert(0,'/home/claude/gen')
import speaklo_ar2 as M
from speaklo_ar2 import NAVY,YEL,CREAM,AR,LA
from PIL import Image,ImageFont
K=M.S;Wd=1080*K;Hd=1920*K
DJ=lambda n:ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",n*K)
def canvas():
    im=Image.new("RGB",(Wd,Hd),NAVY);d=M.ImageDraw.Draw(im);M.chip(d,"كلمة اليوم",YEL,NAVY,x=60,y=120)
    d.rounded_rectangle((60*K,1700*K,116*K,1756*K),radius=18*K,fill=YEL);M.text(d,"s",LA(36),88,1704,NAVY,False);M.text(d,"Speaklo",LA(34),200,1702,CREAM,False);return im,d
def fin(im,p): im.resize((1080,1920),Image.LANCZOS).save(p)
def make(word,ipa,ar,ex,exar,mp4):
    out="/home/claude/gen/reel_"+word;os.makedirs(out,exist_ok=True)
    im,d=canvas();M.text(d,word.upper(),M.fit(d,word.upper(),170,920,False,lambda s:LA(s)),540,760,YEL,False);fin(im,out+"/s1.png")
    im,d=canvas();M.text(d,word.upper(),LA(110),540,560,YEL,False);M.text(d,ipa,DJ(56),540,780,CREAM,False);M.text(d,ar,AR(130),540,960,CREAM);fin(im,out+"/s2.png")
    im,d=canvas();M.text(d,word.upper(),LA(110),540,360,YEL,False)
    d.rounded_rectangle((70*K,640*K,1010*K,1140*K),radius=50*K,fill=(40,58,100))
    y=M.block(d,ex,LA(58,"Medium"),540,720,CREAM,820,False,18);M.block(d,exar,AR(52,"Medium"),540,y+30,YEL,820);fin(im,out+"/s3.png")
    im,d=canvas();M.text(d,word.upper(),LA(110),540,500,YEL,False);M.block(d,"اكتب جملتك بالكلمة دي في الكومنتات",AR(72),540,800,CREAM,860);M.text(d,"تابع Speaklo",AR(56,"Medium"),540,1250,YEL);fin(im,out+"/s4.png")
    ins=[];fc=[]
    for i in range(4):
        ins+=["-i",f"{out}/s{i+1}.png"]
        fc.append(f"[{i}:v]scale=2160:3840,zoompan=z='min(zoom+0.0007,1.09)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=108:s=1080x1920:fps=30,fade=t=in:st=0:d=0.35,fade=t=out:st=3.25:d=0.35[v{i}]")
    fcs=";".join(fc)+";[v0][v1][v2][v3]concat=n=4:v=1:a=0,format=yuv420p[v]"
    cmd=["ffmpeg","-y","-loglevel","error"]+ins+["-f","lavfi","-t","14.4","-i","anullsrc=r=44100:cl=stereo","-filter_complex",fcs,"-map","[v]","-map","4:a","-c:v","libx264","-preset","medium","-crf","20","-c:a","aac","-shortest","-movflags","+faststart",mp4]
    subprocess.run(cmd,check=True)
if __name__=="__main__":
    R="/home/claude/speaklo-media/reels/"
    make("prefer","/prɪˈfɜːr/","يفضّل","I prefer tea to coffee.","أفضّل الشاي على القهوة.",R+"2026-10-23_word_prefer.mp4")
    make("suggest","/səɡˈdʒɛst/","يقترح","I suggest we leave early.","أقترح نمشي بدري.",R+"2026-10-24_word_suggest.mp4")
