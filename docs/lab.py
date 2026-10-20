"""Decimal reconciliation: field policies, tolerance frontier and investigation ledger."""
import json,csv,io
from decimal import Decimal
from common import *

def run(p):
    from engine import index
    sh,sr=read_csv(p.get('source',''));th,tr=read_csv(p.get('target',''));keys=columns(p.get('keys'),sh)
    if not keys:raise ValueError('Choose at least one key column.')
    columns(','.join(keys),th)
    fields=columns(p.get('compare'),sh) or [c for c in sh if c in th and c not in keys];columns(','.join(fields),th)
    absolute=number(p.get('tolerance','0'));relative=number(p.get('relative','0'))
    if absolute is None or relative is None or absolute<0 or not 0<=relative<=100:raise ValueError('Absolute tolerance must be nonnegative; relative tolerance must be 0–100%.')
    normalize=bool(p.get('normalize',False));left=index(sr,keys,'Source');right=index(tr,keys,'Target');records=[];diffs=[];deltas=[];fieldcounts=Counter()
    def equivalent(a,b,atol):
        an,bn=number(a),number(b)
        if an is not None and bn is not None:return abs(an-bn)<=max(atol,relative/100*abs(an))
        return a.strip().casefold()==b.strip().casefold() if normalize else a==b
    for key in sorted(left.keys()|right.keys()):
        a=left.get(key);b=right.get(key);status='target_only' if a is None else 'missing' if b is None else 'matched';cells=[]
        if a is not None and b is not None:
            for c in fields:
                av,bv=a[c],b[c];an,bn=number(av),number(bv);delta=abs(an-bn) if an is not None and bn is not None else None;equal=equivalent(av,bv,absolute)
                if delta is not None:deltas.append((c,delta))
                cells.append({'column':c,'source':av,'target':bv,'equal':equal,'delta':str(delta) if delta is not None else None})
                if not equal:status='changed';fieldcounts[c]+=1;diffs.append([' | '.join(key),'Value mismatch',c,av,bv,str(delta) if delta is not None else 'text'])
        else:diffs.append([' | '.join(key),status,'—',json.dumps(a) if a else '—',json.dumps(b) if b else '—','—'])
        records.append({'key':' | '.join(key),'key_values':list(key),'status':status,'source':a,'target':b,'cells':cells})
    counts=Counter(r['status'] for r in records)
    frontier=[]
    for mul in [Decimal('0'),Decimal('.25'),Decimal('.5'),Decimal('1'),Decimal('2'),Decimal('5'),Decimal('10')]:
        t=absolute*mul if absolute else mul/100
        match=sum(all(equivalent(left[k][c],right[k][c],t) for c in fields) for k in left.keys()&right.keys())
        frontier.append({'tolerance':str(t),'matching':match,'changed':len(left.keys()&right.keys())-match})
    totals=[]
    for c in fields:
        av=[number(r[c]) for r in sr];bv=[number(r[c]) for r in tr]
        if all(v is not None for v in av+bv):
            a=sum(av,Decimal(0));b=sum(bv,Decimal(0));totals.append({'column':c,'source':str(a),'target':str(b),'delta':str(b-a)})
    buf=io.StringIO();w=csv.writer(buf);w.writerow(['key','status','column','source','target','absolute_delta']);w.writerows(diffs)
    out=result('Reconciliation investigation complete',[metric('Matching',counts['matched']),metric('Changed',counts['changed']),metric('Missing',counts['missing']),metric('Target only',counts['target_only'])],['Key','Status','Column','Source','Target','Delta'],diffs,[finding('info','Tolerance is a business policy','Numeric match: absolute delta ≤ max(absolute tolerance, relative % × absolute source value). Text normalization is optional. No dataset is modified.')],artifacts=[{'name':'exception-ledger.csv','content':buf.getvalue()},{'name':'comparison-policy.json','content':json.dumps({'keys':keys,'fields':fields,'absolute':str(absolute),'relative_percent':str(relative),'normalize_text':normalize},indent=2)}])
    out['lab']={'records':records,'counts':dict(counts),'frontier':frontier,'totals':totals,'fields':fields,'field_counts':dict(fieldcounts),'source_count':len(sr),'target_count':len(tr)};return out
from collections import Counter
