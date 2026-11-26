import numpy as np,asr,subprocess,sys,json
from asr import *
def logmel_n(a,n):
    a=np.pad(a,(0,max(0,n*160-len(a))))[:n*160]
    win=np.hanning(401)[:-1].astype(np.float32);p=np.pad(a,(200,200),mode='reflect')
    k=1+(len(p)-400)//160;idx=np.arange(400)[None,:]+160*np.arange(k)[:,None]
    S=np.abs(np.fft.rfft(p[idx]*win,axis=1))**2;S=S[:-1].T;m=MF@S
    l=np.log10(np.maximum(m,1e-10));l=np.maximum(l,l.max()-8.0);return ((l+4)/4).astype(np.float32)[None]
def tr(a,lang,frames):
    ck,cv=enc.run(None,{"mel":logmel_n(a,frames)})
    lt=LANG[lang];cur=np.array([[50258,lt,50360,50364]],np.int64)
    kc=np.zeros((4,1,448,1280),np.float32);vc=kc.copy();out=[];off=0
    for _ in range(80):
        lg,kc,vc=dec.run(None,{"tokens":cur,"in_n_layer_self_k_cache":kc,"in_n_layer_self_v_cache":vc,"n_layer_cross_k":ck,"n_layer_cross_v":cv,"offset":np.array([off],np.int64)})
        l=lg[0,-1].copy();l[sup]=-1e9;l[50258:]=-1e9;t=int(l.argmax());off+=cur.shape[1]
        if t==50257:break
        out.append(t);cur=np.array([[t]],np.int64)
    return decode_tokens(out).strip()
if __name__=="__main__":
    import time
    a=load("wav/vo1.wav")
    for fr in (3000,1500,800):
        t=time.time();print(fr,tr(a[int(3.09*16000):int(5.76*16000)],"ar",fr),round(time.time()-t,1),flush=True)
