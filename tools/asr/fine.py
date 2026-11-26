import sys,numpy as np
sys.argv_=sys.argv
from asr import load
def fine(i,thr=-36,gap=0.11):
    a=load(f"wav/vo{i}.wav");hop=160;n=len(a)//hop
    e=np.array([np.sqrt(np.mean(a[k*hop:(k+1)*hop]**2)+1e-12) for k in range(n)]);db=20*np.log10(e);sp=db>thr
    out=[];s=None;last=None
    for k,v in enumerate(sp):
        t=k*hop/16000
        if v:
            if s is None:s=t
            last=t+0.01
        elif s is not None and t-last>gap:out.append((round(s,2),round(last,2)));s=None
    if s is not None:out.append((round(s,2),round(last,2)))
    return out
for i in map(int,sys.argv[1:]):print(i,fine(i))
