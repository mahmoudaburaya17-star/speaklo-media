import sys,json,numpy as np,subprocess
from seg import *
def segs(i,thr=-38,gap=0.30):
    a=load(f"wav/vo{i}.wav");hop=160;n=len(a)//hop
    e=np.array([np.sqrt(np.mean(a[k*hop:(k+1)*hop]**2)+1e-12) for k in range(n)]);db=20*np.log10(e);sp=db>thr
    out=[];s=None;last=None
    for k,v in enumerate(sp):
        t=k*hop/16000
        if v:
            if s is None:s=t
            last=t+0.01
        elif s is not None and t-last>gap:out.append((s,last));s=None
    if s is not None:out.append((s,last))
    return a,out
if __name__=="__main__":
  for i in map(int,sys.argv[1:]):
      a,ss=segs(i);res=[]
      for s,e in ss:
          x=a[max(0,int((s-0.15)*16000)):int((e+0.15)*16000)]
          if len(x)>14*16000:x=x[:14*16000]
          res.append({"s":round(s,2),"e":round(e,2),"ar":tr(x,"ar",1500),"en":tr(x,"en",1500)})
      json.dump(res,open(f"seg{i}.json","w"),ensure_ascii=False,indent=0);print("done",i,flush=True)
