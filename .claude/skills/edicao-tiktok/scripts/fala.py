import numpy as np, wave, json, sys
def env(f):
    w=wave.open(f"audio/IMG_{f}.wav"); x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768
    hop=160  # 10 ms
    n=len(x)//hop; r=np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1)+1e-10)
    db=20*np.log10(r)
    return db
def speech(f, a, b, rel=13, minsil=0.25, minsp=0.08):
    db=env(f); floor=np.percentile(db,95)
    th=floor-19
    i0,i1=int(a*100),int(b*100)
    on=db[i0:i1]>th
    # smooth: fill short gaps
    iv=[];s=None
    for k,v in enumerate(on):
        t=(i0+k)/100
        if v and s is None: s=t
        if not v and s is not None: iv.append([s,t]); s=None
    if s is not None: iv.append([s,b])
    m=[]
    for s,e in iv:
        if m and s-m[-1][1]<minsil: m[-1][1]=e
        else: m.append([s,e])
    return [x for x in m if x[1]-x[0]>=minsp], floor
if __name__=="__main__":
    f,a,b=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
    ws=[w for s in json.load(open(f"audio/IMG_{f}.m.json")) for w in s["words"]]
    iv,fl=speech(f,a,b)
    print("floor",round(fl,1))
    for s,e in iv:
        inw=[w["word"].strip() for w in ws if s-0.05<=(w["start"]+w["end"])/2<=e+0.05]
        print(f"{s:6.2f}-{e:6.2f} {' '.join(inw) or '<<SEM PALAVRA>>'}")
