import sys, base64, subprocess, numpy as np, onnxruntime as ort
D="/home/claude/asr/sherpa-onnx-whisper-turbo/"
so=ort.SessionOptions(); so.intra_op_num_threads=2
enc=ort.InferenceSession(D+"turbo-encoder.int8.onnx",so,providers=["CPUExecutionProvider"])
dec=ort.InferenceSession(D+"turbo-decoder.int8.onnx",so,providers=["CPUExecutionProvider"])
meta=enc.get_modelmeta().custom_metadata_map
codes=meta['all_language_codes'].split(','); ltoks=[int(x) for x in meta['all_language_tokens'].split(',')]
LANG=dict(zip(codes,ltoks))
sup=[int(x) for x in meta['non_speech_tokens'].split(',')]
toks=[base64.b64decode(l.split()[0]) for l in open(D+"turbo-tokens.txt")]
def mel_filters(sr=16000,n_fft=400,n_mels=128):
    fmin,fmax=0.0,sr/2
    def h2m(f):
        f=np.asarray(f,float); m=f/(200/3); lg=np.log(6.4)/27
        return np.where(f>=1000,15+np.log(np.maximum(f,1e-9)/1000)/lg,m)
    def m2h(m):
        m=np.asarray(m,float); lg=np.log(6.4)/27
        return np.where(m>=15,1000*np.exp(lg*(m-15)),m*(200/3))
    mels=np.linspace(h2m(fmin),h2m(fmax),n_mels+2); fm=m2h(mels)
    ff=np.linspace(0,sr/2,1+n_fft//2)
    fd=np.diff(fm); ramps=fm[:,None]-ff[None,:]
    w=np.zeros((n_mels,len(ff)))
    for i in range(n_mels):
        lo=-ramps[i]/fd[i]; up=ramps[i+2]/fd[i+1]
        w[i]=np.maximum(0,np.minimum(lo,up))
    w*= (2.0/(fm[2:n_mels+2]-fm[:n_mels]))[:,None]
    return w.astype(np.float32)
MF=mel_filters()
def logmel(a):
    a=np.pad(a,(0,480000)); a=a[:480000]
    win=np.hanning(401)[:-1].astype(np.float32)
    p=np.pad(a,(200,200),mode='reflect')
    n=1+(len(p)-400)//160
    idx=np.arange(400)[None,:]+160*np.arange(n)[:,None]
    S=np.abs(np.fft.rfft(p[idx]*win,axis=1))**2
    S=S[:-1].T
    m=MF@S
    l=np.log10(np.maximum(m,1e-10)); l=np.maximum(l,l.max()-8.0)
    return ((l+4)/4).astype(np.float32)[None]
def load(f):
    r=subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True)
    return np.frombuffer(r.stdout,np.float32)
def decode_tokens(ids):
    return b"".join(toks[i] for i in ids if i<50257).decode("utf-8","ignore")
def transcribe(f,lang=None,maxtok=220):
    a=load(f)
    ck,cv=enc.run(None,{"mel":logmel(a[:480000])})
    if lang is None:
        lg=dec.run(None,{"tokens":np.array([[50258]],np.int64),"in_n_layer_self_k_cache":np.zeros((4,1,448,1280),np.float32),"in_n_layer_self_v_cache":np.zeros((4,1,448,1280),np.float32),"n_layer_cross_k":ck,"n_layer_cross_v":cv,"offset":np.array([0],np.int64)})[0][0,-1]
        m=np.full_like(lg,-1e9); 
        for t in ltoks: m[t]=lg[t]
        lt=int(m.argmax()); lang=codes[ltoks.index(lt)]
    lt=LANG[lang]
    seq=[50258,lt,50360,50364]
    kc=np.zeros((4,1,448,1280),np.float32); vc=kc.copy()
    out=[]; cur=np.array([seq],np.int64); off=0
    for _ in range(maxtok):
        lg,kc,vc=dec.run(None,{"tokens":cur,"in_n_layer_self_k_cache":kc,"in_n_layer_self_v_cache":vc,"n_layer_cross_k":ck,"n_layer_cross_v":cv,"offset":np.array([off],np.int64)})
        l=lg[0,-1].copy(); l[sup]=-1e9; l[50257+1:]=-1e9 if False else l[50257+1:]
        l[50258:]=-1e9
        t=int(l.argmax()); 
        off+=cur.shape[1]
        if t==50257: break
        out.append(t); cur=np.array([[t]],np.int64)
    return lang,decode_tokens(out)
if __name__=="__main__":
    for f in sys.argv[1:]:
        for L in (None,):
            print(f.split('/')[-1],*transcribe(f,L),flush=True)
