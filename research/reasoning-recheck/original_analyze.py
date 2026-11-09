"""Paired comparison with the saved original answers; no outcome-selected cases."""
from pathlib import Path
from fractions import Fraction as F
import json,re,sys,hashlib
import numpy as np
from controlled.score import score as frozen_score
ROOT=Path(__file__).resolve().parent
def load(p):return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
def score(p,r,mode='strict'):
    p={**p,'gold_rows':[{**v,'a_percent':F(v['a_percent'])} for v in p['gold_rows']]}
    raw=r.get('raw_text');r={**r}
    if mode!='strict' and isinstance(raw,str):
        s=raw.strip();m=re.fullmatch(r'```(?:json)?\s*(.*?)\s*```',s,re.S)
        if m:s=m[1]
        try:
            obj=json.loads(s)
            if isinstance(obj,dict) and 'rows' not in obj and isinstance(obj.get('lots'),list):obj['rows']=obj.pop('lots')
            r['raw_text']=json.dumps(obj)
        except (ValueError,TypeError):pass
    if r.get('response',{}).get('choices',[{}])[0].get('finish_reason')=='length':r['raw_text']=None
    return frozen_score(p,r)
def main():
    cfg=json.loads((ROOT/'data/protocol.json').read_text());ps=load(ROOT/'data/prompts.jsonl')
    rs=load(ROOT/'results/evaluation/raw.jsonl');old=load(ROOT/'data/baseline_raw.jsonl');pm={p['request_id']:p for p in ps};rm={r['request_id']:r for r in rs};om={r['request_id']:r for r in old}
    assert len(rm)==len(rs)==100 and set(rm)==set(pm)==set(om),'Full evaluation required'
    for path,h in cfg['files'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,path
    scored=[];summaries=[]
    for mode in ['strict','format_only']:
        for label,source in [('original',om),('thinking',rm)]:
            rows=[{'request_id':p['request_id'],'corpus':p['corpus'],'method':p['method'],'family':p['family'],'structure':p.get('structure'),'representation':p['representation'],**score(p,source[p['request_id']],mode)} for p in ps]
            scored.extend({'view':mode,'configuration':label,**r} for r in rows)
            sets=[('controlled_homogeneous',[r for r in rows if r['corpus']=='controlled' and r['structure']=='homogeneous']),('controlled_heterogeneous',[r for r in rows if r['corpus']=='controlled' and r['structure']=='heterogeneous']),('source_direct',[r for r in rows if r['corpus']=='source' and r['method']=='direct']),('source_ledger',[r for r in rows if r['corpus']=='source' and r['method']=='ledger'])]
            sets.extend((f'source_{method}_{representation}',[r for r in rows if r['corpus']=='source' and r['method']==method and r['representation']==representation]) for method in ['direct','ledger'] for representation in ['merged','fragmented'])
            result={'view':mode,'configuration':label,'groups':{}}
            for name,ss in sets:
                result['groups'][name]={'n':len(ss),'answer_correct':sum(r['answer_correct'] for r in ss),'valid_answer':sum(r['direct_valid'] for r in ss)}
                if name.startswith('source_ledger'):
                    result['groups'][name].update({k:sum(r[k] for r in ss) for k in ['ledger_valid','ledger_exact','calculator_correct','correct_total_wrong_valid_ledger']})
                    result['groups'][name]['fields_right_total_wrong']=sum(r['ledger_exact'] and not r['answer_correct'] for r in ss)
            fams=sorted({r['family'] for r in rows if r['corpus']=='controlled'})
            differences=[]
            for fam in fams:
                a={r['structure']:int(r['answer_correct']) for r in rows if r['corpus']=='controlled' and r['family']==fam};differences.append(a['homogeneous']-a['heterogeneous'])
            rng=np.random.default_rng(cfg['seed']);vals=np.array(differences);boots=vals[rng.integers(0,len(vals),size=(10000,len(vals)))].mean(axis=1)
            result['homogeneous_minus_heterogeneous_pp']=100*vals.mean();result['family_bootstrap_95_pp']=(100*np.quantile(boots,[.025,.975])).tolist();summaries.append(result)
    paired={}
    for mode in ['strict','format_only']:
        for corpus,method in [('controlled','direct'),('source','direct'),('source','ledger')]:
            pps=[p for p in ps if p['corpus']==corpus and p['method']==method];trans={'both_correct':0,'correct_to_wrong':0,'wrong_to_correct':0,'both_wrong':0}
            for p in pps:
                before=score(p,om[p['request_id']],mode)['answer_correct'];after=score(p,rm[p['request_id']],mode)['answer_correct'];key='both_correct' if before and after else 'correct_to_wrong' if before else 'wrong_to_correct' if after else 'both_wrong';trans[key]+=1
            paired[f'{mode}_{corpus}_{method}']=trans
    failures=[]
    for p in ps:
        s=score(p,rm[p['request_id']],'format_only')
        if not s['answer_correct'] or (p['method']=='ledger' and not s['ledger_exact']):failures.append({'request_id':p['request_id'],'corpus':p['corpus'],'method':p['method'],'raw_text':rm[p['request_id']].get('raw_text'),'gold_percent_exact':p['gold_percent_exact'],'gold_rows':p['gold_rows'],**s})
    report={'status':'COMPLETE','evaluation_calls':len(rs),'summaries':summaries,'paired_transitions':paired,'request_errors':sum(r['status']!='response_received' for r in rs),'truncated':sum(r.get('response',{}).get('choices',[{}])[0].get('finish_reason')=='length' for r in rs),'nonempty_reasoning':sum(bool(r.get('reasoning_text')) for r in rs),'format_only_failure_census':failures,'note':'A configuration stress test on previously observed inputs, not a pure thinking-mode causal experiment, new blind benchmark, or proof of equivalence. Bootstrap intervals resample these 24 families; a degenerate zero interval at ceiling must not be read as evidence of population equivalence.'}
    (ROOT/'results/scored.jsonl').write_text(''.join(json.dumps(s)+'\n' for s in scored));(ROOT/'results/analysis.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
