import sys
from seg import *
from segall import segs
i=int(sys.argv[1]);langs=sys.argv[2].split(',')
a,ss=segs(i)
for n,(s,e) in enumerate(ss):
    x=a[max(0,int((s-0.15)*16000)):int((e+0.15)*16000)][:14*16000]
    print(n,round(s,2),round(e,2),*[l+": "+tr(x,l,1500) for l in langs],flush=True)
