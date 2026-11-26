"""spec -> cfg object for short_auto. spec keys: wav, chip, total, emoji, hook=[(text,size,color,is_ar)],
segments: list of (a,b,text,caption)  (times from the voiceover)
cards: list of dict(seg=index in segments, en=, ar=, color=, tag=, scene=n)  (scene groups of <=3)
"""
import sys,types
sys.path.insert(0,'/home/claude/gen')
from short_lib import prop
from fx import MINT,YEL,CORAL
COLS=[MINT,YEL,CORAL]
def build(sp):
    C=types.SimpleNamespace();C.VOICE=sp["wav"];C.CHIP=sp["chip"];C.TOTAL=sp["total"]
    C.SEGS=[]
    for a,b,t,cap in sp["segments"]:
        if isinstance(t,list):ws=t
        else:ws=prop(a,b,t)
        C.SEGS.append((a,b,ws,cap))
    C.ROWS=[];groups={}
    for n,c in enumerate(sp["cards"]):
        if "ent" in c:
            a0,b0=c["ent"];C.SEGS.append((a0,b0,prop(a0,b0,c["en"]),False));c["seg"]=len(C.SEGS)-1
        a=C.SEGS[c["seg"]][0]
        C.ROWS.append((c["en"],c["ar"],c.get("color",COLS[n%3]),c["seg"],a-0.3 if "t" not in c else c["t"],c.get("tag")))
        groups.setdefault(c.get("scene",0),[]).append(n)
    ks=sorted(groups);C.SCENES=[]
    h0=sp["segments"][0][0]
    first=min(r[4] for r in C.ROWS)
    C.SCENES.append(("hook",0.0,max(1.5,first-0.05),dict(emoji=sp["emoji"],lines=sp["hook"])))
    for i,k in enumerate(ks):
        a=C.ROWS[groups[k][0]][4]-0.05 if i>0 else C.SCENES[0][2]
        if i>0:C.SCENES[-1]=(C.SCENES[-1][0],C.SCENES[-1][1],a,*C.SCENES[-1][3:])
        C.SCENES.append(("cards",a,None,groups[k]))
    cta=sp["cta"];C.SCENES[-1]=(C.SCENES[-1][0],C.SCENES[-1][1],cta,*C.SCENES[-1][3:])
    C.SCENES.append(("cta",cta,sp["total"]))
    return C
