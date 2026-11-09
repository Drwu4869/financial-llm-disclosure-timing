"""Independent exact-arithmetic checker; no optimizer, NumPy or model required."""
from fractions import Fraction as F
import json,re,hashlib
from pathlib import Path

def bounds(record):
    X=[[F(v) for v in row] for row in record['X']];y=list(map(F,record['y']))
    p=list(map(F,record['primal_weights']));lam=list(map(F,record['dual_weights']))
    assert len(X)==len(y)==len(lam) and all(len(row)==len(p) for row in X)
    assert all(v>=0 for v in p) and sum(p)==1
    assert sum(abs(v) for v in lam)<=1
    upper=max(abs(sum(a*b for a,b in zip(row,p))-z) for row,z in zip(X,y))
    lower=max(F(0),sum(a*b for a,b in zip(lam,y))-max(sum(lam[t]*X[t][j] for t in range(len(X))) for j in range(len(p))))
    assert F(record['lower_exact'])==lower and F(record['upper_exact'])==upper
    assert upper>=lower
    assert upper-lower<=F(1,10**7)
    return lower,upper

def main():
    folder=Path(__file__).resolve().parent/'results/certificates'
    rs=[json.loads(l) for l in (folder/'certificates.jsonl').read_text().splitlines()]
    assert len(rs)==86 and len({(r['model'],r['mode'],r['case_id']) for r in rs})==86
    root=folder.parents[1]
    prompts={r['request_id']:r for r in map(json.loads,(root/'data/prompts.jsonl').read_text().splitlines())}
    raw={}
    for model in ['smol','qwen8']:
        rr={r['request_id']:r for r in map(json.loads,(root/f'results/{model}/prompts_evaluation/raw.jsonl').read_text().splitlines())}
        if model=='qwen8':
            extra={r['request_id']:r for r in map(json.loads,(root/f'results/{model}/runtime_recheck_prompts_evaluation/raw.jsonl').read_text().splitlines())}
            protocol=json.loads((root/'data/runtime_recheck_protocol.json').read_text())
            assert set(extra)==set(protocol['selected_request_ids']) and len(extra)==167
            rr.update(extra)
        raw[model]=rr
    for r in rs:
        bounds(r)
        for t,rid in enumerate(r['request_ids']):
            record=raw[r['model']][rid]
            assert record['request_sha256']==r['raw_payload_hashes'][t]
            assert hashlib.sha256(record['raw_text'].encode()).hexdigest()==r['raw_text_hashes'][t]
            answer=json.loads(record['raw_text'],parse_float=F,parse_int=F)
            y=answer['a']/(answer['a']+answer['b']) if r['mode']=='normalized' else answer['a']
            assert F(r['y'][t])==y
            extracted={}
            for line in prompts[rid]['prompt'].splitlines():
                hit=re.search(r'Product_(\d+)',line)
                if hit:
                    value=re.search(r'(\d+\.\d+)% to Asset_A|Asset_A (\d+\.\d+)%',line)
                    assert value
                    extracted[int(hit[1])]=F(value[1] or value[2])/100
            assert [F(z) for z in r['X'][t]]==[extracted[j] for j in range(1,5)]
    print(json.dumps({'status':'PASS','certificates':len(rs),'method':'exact rational arithmetic; no optimizer','max_gap':float(max(bounds(r)[1]-bounds(r)[0] for r in rs))}))

if __name__=='__main__':main()
