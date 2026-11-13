"""Shared Speaklo Reel quality kit (v2): safe zones, animated brand background, easing, light SFX + soft pad music, loudness-normalised encode."""
import math,subprocess,wave
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
NAVY=(27,42,78);PANEL=(38,56,100);YEL=(255,201,60);CORAL=(255,107,74);MINT=(46,196,182);CREAM=(255,248,238);DIM=(125,142,182)
FD="/usr/share/fonts/truetype/google-fonts/";G="/home/claude/gen/"
W,H,FPS,SR=1080,1920,24,24000
# Facebook Reels UI covers ~bottom 340 px and the right ~130 px (lower half): keep text inside x 80..1000, y 120..1580
SAFE_BOTTOM=1580
def LA(s,w="Bold"):return ImageFont.truetype(FD+f"Poppins-{w}.ttf",s)
def AR(s,w="Medium"):return ImageFont.truetype(G+f"Tajawal-{w}.ttf",s,layout_engine=ImageFont.Layout.RAQM)
def ar(d,xy,t,size,fill,w="Bold",anchor="mm"):d.text(xy,t,font=AR(size,w),fill=fill,anchor=anchor,direction="rtl",language="ar")
def emoji(ch,size=300):
    f=ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",109)
    im=Image.new("RGBA",(136,128),(0,0,0,0));ImageDraw.Draw(im).text((0,0),ch,font=f,embedded_color=True)
    return im.resize((int(136*size/128),size),Image.LANCZOS)
def clamp(x,a=0.0,b=1.0):return max(a,min(b,x))
def ease_out_back(t,s=1.70158):t=clamp(t)-1;return 1+(s+1)*t**3+s*t**2
def ease_out_cubic(t):t=clamp(t);return 1-(1-t)**3
def fade(spr,a):
    if a>=0.999:return spr
    spr=spr.copy();spr.putalpha(spr.getchannel("A").point(lambda v:int(v*clamp(a))));return spr
def make_bg():
    S=(1500,2400);base=Image.new("RGB",S,NAVY);ov=Image.new("RGBA",S,(0,0,0,0));d=ImageDraw.Draw(ov)
    for x,y,r,c in [(300,500,430,CORAL),(1250,950,500,MINT),(450,1750,520,YEL),(1150,2150,380,CORAL)]:d.ellipse((x-r,y-r,x+r,y+r),fill=c+(44,))
    ov=ov.filter(ImageFilter.GaussianBlur(130));base.paste(ov,(0,0),ov);return base
def bg_frame(layer,T):
    ox=int(210+120*math.sin(T*0.35));oy=int(240+140*math.cos(T*0.28));return layer.crop((ox,oy,ox+W,oy+H)).copy()
def progress(im,T,total):
    d=ImageDraw.Draw(im);d.rounded_rectangle((120,1572,960,1584),6,fill=PANEL);w=int(840*clamp(T/total))
    if w>12:d.rounded_rectangle((120,1572,120+w,1584),6,fill=YEL)
# ---- audio ----
def pop():
    t=np.arange(int(0.2*SR))/SR;f=720*np.exp(-t*9)+260;return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*20)*0.5
def whoosh():
    n=int(0.4*SR);rng=np.random.default_rng(3);x=rng.standard_normal(n);k=np.ones(18)/18;x=np.convolve(x,k,"same")
    env=np.sin(np.linspace(0,np.pi,n))**2;return x*env*0.55
def bgm(total):
    n=int((total+1)*SR);out=np.zeros(n);prog=[(55.0,65.41,82.41),(43.65,65.41,87.31),(65.41,82.41,98.0),(49.0,73.42,98.0)];L=3.6
    for i in range(int(total/L)+2):
        a=prog[i%4];s=int(i*L*SR)
        if s>=n:break
        m=int((L+0.8)*SR);t=np.arange(m)/SR
        env=np.minimum(t/0.7,1)*np.minimum((L+0.8-t)/0.8,1)
        ch=sum(np.sin(2*np.pi*f*t)+0.35*np.sin(2*np.pi*2*f*t) for f in a)/3
        seg=ch*env*0.07;e=min(n,s+m);out[s:e]+=seg[:e-s]
    return out
def mix(total,voices,sfx,path):
    """voices=[(start_s,wav)], sfx=[(start_s,np_array)]"""
    n=int((total+1)*SR);a=bgm(total)[:n]
    for s,w in voices:
        x=np.frombuffer(wave.open(w).readframes(10**8),dtype=np.int16)/32768;i=int(s*SR);a[i:i+len(x)]+=x
    for s,x in sfx:
        i=int(s*SR);a[i:i+len(x)]+=x*0.6
    with wave.open(path,"wb") as o:o.setnchannels(1);o.setsampwidth(2);o.setframerate(SR);o.writeframes((np.clip(a,-1,1)*32767).astype(np.int16).tobytes())
def encode(total,frame_fn,wav,out):
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",wav,"-c:v","libx264","-pix_fmt","yuv420p","-preset","fast","-crf","19","-c:a","aac","-b:a","160k","-af","loudnorm=I=-16:TP=-1.5:LRA=11","-t",f"{total:.2f}","-movflags","+faststart",out],stdin=subprocess.PIPE)
    for fr in range(int(total*FPS)):p.stdin.write(frame_fn(fr/FPS).tobytes())
    p.stdin.close();p.wait()
