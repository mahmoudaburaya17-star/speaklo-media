import sys,importlib,time
sys.path.insert(0,'/home/claude/gen');sys.path.insert(0,'/home/claude/gen/specs')
import mk,short_auto
n=sys.argv[1];out=sys.argv[2]
m=importlib.import_module("s"+n);t=time.time()
short_auto.main(mk.build(m.SP),out);print("done",round(time.time()-t))
