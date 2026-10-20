"""Key-based CSV reconciliation with strict key checks and decimal tolerance."""
import csv,io
from common import *

def index(rows,keys,label):
    out={}
    for i,row in enumerate(rows,2):
        k=tuple(row[c].strip()for c in keys)
        if any(not v for v in k):raise ValueError(f'{label}: blank key at record {i}.')
        if k in out:raise ValueError(f'{label}: duplicate key {k}; choose a unique composite key.')
        out[k]=row
    return out

def legacy_run(p):
    sh,sr=read_csv(p.get('source',''));th,tr=read_csv(p.get('target',''))
    keys=columns(p.get('keys'),sh)
    if not keys:raise ValueError('Choose at least one key column (comma-separated).')
    columns(','.join(keys),th)
    compare=columns(p.get('compare'),sh)or[c for c in sh if c in th and c not in keys]
    columns(','.join(compare),th)
    tolerance=number(p.get('tolerance','0'))
    if tolerance is None or tolerance<0:raise ValueError('Tolerance must be a finite non-negative number.')
    left=index(sr,keys,'Source');right=index(tr,keys,'Target');out=[];changed=0;matched=0
    for k in sorted(left.keys()|right.keys()):
        key=' | '.join(k)
        if k not in right:out.append([key,'Missing in target','—','Source record','—']);continue
        if k not in left:out.append([key,'Target only','—','—','Target record']);continue
        differences=[]
        for c in compare:
            a,b=left[k][c],right[k][c];an,bn=number(a),number(b)
            equal=abs(an-bn)<=tolerance if an is not None and bn is not None else a==b
            if not equal:differences.append(c);out.append([key,'Value mismatch',c,a,b])
        if differences:changed+=1
        else:matched+=1
    missing=len(left.keys()-right.keys());extra=len(right.keys()-left.keys());findings=[]
    if sh!=th:findings.append(finding('warning','Schema differs','Source-only: '+(', '.join(c for c in sh if c not in th)or 'none')+'; target-only: '+(', '.join(c for c in th if c not in sh)or 'none')+'. Column order may also differ.'))
    if missing or extra or changed:findings.append(finding('warning','Reconciliation exceptions found','Review missing keys separately from value mismatches; no data is automatically modified.'))
    else:findings.append(finding('success','All compared records match','Numeric comparisons use the chosen absolute tolerance; text comparisons are exact.'))
    if not compare:findings.append(finding('info','Key-presence comparison only','There are no shared non-key columns to compare.'))
    buf=io.StringIO();w=csv.writer(buf);w.writerow(['key','status','column','source','target']);w.writerows(out)
    return result('Reconciliation complete',[metric('Matching records',matched),metric('Changed records',changed),metric('Missing in target',missing),metric('Target only',extra)],['Key','Status','Column','Source','Target'],out,findings,[{'label':'Matching','value':matched},{'label':'Changed','value':changed},{'label':'Missing','value':missing},{'label':'Target only','value':extra}],[{'name':'reconciliation.csv','content':buf.getvalue()}])


def run(p):
    if not isinstance(p,dict):raise ValueError("Send a JSON object.")
    if p.get("workspace")=="studio":
        from lab import run as studio_run
        return studio_run(p)
    return legacy_run(p)
