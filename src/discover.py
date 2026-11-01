"""Hybrid ranker: concept-augmented TF-IDF similarity + school-ecosystem signals. Pure Python.
Usage (from repo root): python src/discover.py"""
import re, math, json
from collections import Counter
STOP=set("a an and the of in at for to with on by as is are was were be from or that this their his her its it into across over more than who which have has had also".split())
SYN=dict(headmaster="principal",headmistress="principal",headteacher="principal",adviser="advisor",chairman="trustee",chairperson="trustee",
 promoter="owner",founder="owner",cofounder="owner",entrepreneur="owner",mentor="advisor",coach="advisor",consulting="consultant",consultancy="consultant",
 schools="school",trustees="trustee",principals="principal",directors="director",owners="owner",founded="owner")
R=dict(k12=r"\bk-?12\b|\bcbse\b|\bicse\b|\bigcse\b|\bschools?\b|\bprincipals?\b|headmaster",
 adv=r"consultant|consulting|consultancy|advis[eo]r|advisory|mentor|accreditation|audit",
 lead=r"principal|headmaster|headmistress|school director|head of school|trustee|chairman|owner|founder|founded|promoter",
 net=r"network|group of schools|chain|cluster|multiple schools|campuses|association",
 dec=r"decision-makers?|management|trustees?|owners?|promoters?|principals")
W=dict(adv=.30,lead=.25,multi=.30,dec=.15)
LBL=dict(adv="advisory/consulting role",lead="school leadership background (principal/trustee/owner)",multi="works across multiple schools",dec="engages school decision-makers")
def text(p): return " ".join([p["headline"],p["role"],p["org"],p["summary"]]+p["experience"])
def analyze(t):
    t=t.lower(); t=re.sub(r"(business|medical|law|engineering) school|school of \w+","",t)
    f={k:bool(re.search(v,t)) for k,v in R.items()}
    n=max([int(x) for x in re.findall(r"(\d+)\+?\s+schools",t)]+[0])
    f["multi"]=n>=3 or bool(re.search(R["net"],t)); f["n"]=n
    tok=[SYN.get(w,w) for w in re.findall(r"[a-z0-9\-]+",t) if w not in STOP]
    tok+=["cpt_"+k for k in ("k12","adv","lead","multi","dec") if f[k]]
    return tok,f
def rank(ref_text,cands,top=25):
    docs=[analyze(ref_text)]+[analyze(text(p)) for p in cands]; N=len(docs)
    df=Counter(w for t,_ in docs for w in set(t))
    vec=lambda t:{w:(1+math.log(c))*(math.log((1+N)/(1+df[w]))+1) for w,c in Counter(t).items()}
    V=[vec(t) for t,_ in docs]
    nrm=lambda a:math.sqrt(sum(x*x for x in a.values()))
    cos=lambda a,b:sum(a[w]*b.get(w,0) for w in a)/(nrm(a)*nrm(b)+1e-9)
    sims=[cos(V[0],v) for v in V[1:]]; mx=max(sims) or 1; out=[]
    for p,s,(t,f),v in zip(cands,sims,docs[1:],V[1:]):
        sig=sum(W[k]*f[k] for k in W); gate=1 if f["k12"] else .25
        sc=gate*(.5*s/mx+.5*sig)
        shared=sorted([w for w in v if w in V[0] and not w.startswith("cpt_")],key=lambda w:-v[w]*V[0][w])[:4]
        why=[LBL[k] for k in W if f[k]]
        if f["n"]: why.append(f"~{f['n']} schools mentioned")
        if not f["k12"]: why=["no school-ecosystem signal (filtered)"]
        out.append(dict(p=p,score=round(100*sc),why=why,shared=shared))
    return sorted(out,key=lambda r:-r["score"])[:top]
if __name__=="__main__":
    D=json.load(open("data/profiles.json")); ref=D["reference"]
    res=rank(text(ref),D["profiles"])
    for i,r in enumerate(res,1): print(f'{i:2d} {r["score"]:3d} {r["p"]["name"]:<20} {r["p"]["role"]:<38} | {"; ".join(r["why"])}')
    print(f"\nPrecision@20 (test reference): {sum(r['p']['gt'] for r in res[:20])/20:.2f}")
    ps=[]
    for q in [x for x in D["profiles"] if x["gt"]]:
        r=rank(text(q),[x for x in D["profiles"] if x["id"]!=q["id"]],20); ps.append(sum(x["p"]["gt"] for x in r)/20)
    print(f"Mean Precision@20 over {len(ps)} leave-one-out references: {sum(ps)/len(ps):.2f}")
