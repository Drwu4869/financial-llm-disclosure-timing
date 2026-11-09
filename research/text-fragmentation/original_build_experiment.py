"""Freeze paired synthetic and public-return-grounded stimuli before inference."""
import csv
import hashlib
import itertools
import json
import math
import random
import statistics
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'frozen'
ASSETS = ['Asset_A', 'Asset_B']
SOURCE_URL = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_CSV.zip'
MODEL = 'Qwen/Qwen2.5-1.5B-Instruct-GGUF'
REVISION = '91cad51170dc346986eccefdc2dd33a9da36ead9'


def write_jsonl(path, rows):
    path.write_text(''.join(json.dumps(r, sort_keys=True)+'\n' for r in rows))


def load_jsonl(path):
    return [json.loads(s) for s in Path(path).read_text().splitlines() if s.strip()]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def risk(weights, returns):
    ys = [sum(w*x for w,x in zip(weights,row)) for row in returns]
    return statistics.pstdev(ys)


def public_rows():
    source = ROOT/'data/source/49_Industry_Portfolios_CSV.zip'
    with zipfile.ZipFile(source) as z:
        s = z.read('49_Industry_Portfolios.csv').decode('utf-8-sig')
    start = s.index('Average Value Weighted Returns -- Monthly')
    end = s.index('Average Equal Weighted Returns -- Monthly')
    rows = list(csv.reader(x for x in s[start:end].splitlines()[1:] if x.strip()))
    labels = [v.strip() for v in rows[0][1:]]
    values = {r[0].strip(): [float(x) for x in r[1:]] for r in rows[1:]}
    return labels, values, s.splitlines()[0]


def make_cases():
    labels, observed, vintage = public_rows()
    cases=[]
    for split_index,split in enumerate(['development','evaluation']):
        rng=random.Random(202611040+split_index)
        for domain in ['synthetic','public_returns']:
            for i in range(8):
                cid=f'{split}_{domain}_{i+1:02d}'
                if domain=='synthetic':
                    a=rng.uniform(1,4); b=rng.uniform(1,4); rho=rng.uniform(-.4,.75)
                    returns=[[round(a*x,6),round(b*(rho*x+math.sqrt(1-rho*rho)*y),6)] for x,y,z in itertools.product([-1,1],repeat=3)]
                    provenance={'generator_seed':202611040+split_index,'scale_a':a,'scale_b':b,'rho':rho}
                    horizon='one-day'; row_labels=[str(j+1) for j in range(8)]
                else:
                    left=split_index*16+2*i; columns=[left,left+1]
                    year=2011 if split=='development' else 2021
                    row_labels=[f'{year}{month:02d}' for month in range(1,9)]
                    returns=[[observed[date][j] for j in columns] for date in row_labels]
                    assert all(x not in [-99.99,-999] for row in returns for x in row)
                    provenance={'source_url':SOURCE_URL,'vintage':vintage,'industry_codes':[labels[j] for j in columns],'months':row_labels,'original_column_indices_zero_based':columns}
                    horizon='one-month empirical';
                u=[.8,.85,.9,.75][i%4]
                w1=[u,1-u]; w2=[.5,.5]
                desired='increase' if i%2 else 'decrease'
                low,high=sorted([w1,w2],key=lambda w:risk(w,returns))
                base,control=(low,high) if desired=='increase' else (high,low)
                assert abs(risk(base,returns)-risk(control,returns))>1e-8
                cases.append({'case_id':cid,'family_id':cid,'split':split,'domain':domain,
                    'assets':ASSETS,'returns_pct':returns,'row_labels':row_labels,'horizon':horizon,
                    'base_weights':base,'control_weights':control,'control_direction':desired,'provenance':provenance})
    return cases


def graph(weights, form):
    if form in ['one','canonical']:
        return [(1.,weights)]
    if form in ['eight','matched_one','matched_eight']:
        return [(.125,weights) for _ in range(8)]
    if form=='heterogeneous':
        delta=min(weights)*.5
        offsets=[-1,-.75,-.5,-.25,.25,.5,.75,1]
        return [(.125,[weights[0]+delta*z,weights[1]-delta*z]) for z in offsets]
    raise ValueError(form)


def holdings(weights,form):
    if form=='canonical':
        return f'Aggregate underlying portfolio weights: Asset_A {weights[0]*100:g}%; Asset_B {weights[1]*100:g}%.'
    rows=graph(weights,form)
    lines=[]
    if form.startswith('matched_'):
        lines.append('The account contains eight separately funded accounting lots. Repeated product names denote the same product; every listed lot contributes its stated account weight.')
    for j,(q,w) in enumerate(rows):
        name=1 if form=='matched_one' else j+1
        prefix=f'Lot L{j+1}: ' if form.startswith('matched_') else ''
        lines.append(prefix+f'The account invests {q*100:g}% in product P{name}, which holds {w[0]*100:g}% Asset_A and {w[1]*100:g}% Asset_B.')
    return '\n'.join(lines)


CONDITIONS=[
    ('direct_one','base','one','risk',False),
    ('direct_eight','base','eight','risk',False),
    ('matched_one','base','matched_one','risk',False),
    ('matched_eight','base','matched_eight','risk',False),
    ('canonical','base','canonical','risk',False),
    ('oracle_one','base','one','risk',True),
    ('oracle_eight','base','eight','risk',True),
    ('extract_one','base','one','extract',False),
    ('extract_eight','base','eight','extract',False),
    ('direct_heterogeneous','base','heterogeneous','risk',False),
    ('extract_heterogeneous','base','heterogeneous','extract',False),
    ('control_direct_one','control','one','risk',False),
    ('control_direct_eight','control','eight','risk',False),
    ('control_extract_one','control','one','extract',False),
    ('control_extract_eight','control','eight','extract',False)]


def make_prompts(cases):
    requests=[];gold=[]
    for c in cases:
        for name,economy,form,task,oracle in CONDITIONS:
            w=c[economy+'_weights']
            lines=['All products are bookkeeping containers. There are no fees, taxes, leverage, trading, default, liquidity differences, or other product-specific risks. Each underlying asset has the same return wherever it appears.',holdings(w,form)]
            if task=='risk':
                if c['domain']=='public_returns':
                    lines.append('The table contains eight observed monthly returns for two anonymized industry research portfolios. Treat its rows as an empirical distribution with probability 1/8 each. Compute a descriptive statistic of these observations, not a forecast.')
                else:
                    lines.append('The table contains eight hypothetical joint one-day states, each with probability 1/8.')
                lines.append('All returns are in percent. Row | Asset_A | Asset_B')
                lines += [f'{label} | {r[0]:.6f} | {r[1]:.6f}' for label,r in zip(c['row_labels'],c['returns_pct'])]
                if oracle:lines.append('Verified aggregate underlying weights: '+holdings(w,'canonical'))
                lines.append('Compute the portfolio return POPULATION standard deviation across these eight rows (divide variance by 8, not 7). Report percentage points: 1.25 means 1.25%. Return only {"volatility_pct": number}. If unable, return {"volatility_pct": null}. Do not change the allocation.')
            else:
                lines.append('Aggregate the account exposures through all products and lots. Return only {"weights": {"Asset_A": number, "Asset_B": number}}, using fractions summing to 1 (0.8 means 80%). Count all funded lots and combine repeated underlying assets. Do not estimate risk.')
            prompt='\n'.join(lines)
            rid=c['case_id']+'__'+name
            requests.append({'request_id':rid,'case_id':c['case_id'],'family_id':c['family_id'],'split':c['split'],'domain':c['domain'],'condition':name,'task':task,'system':'Use only the supplied information. Return exactly one JSON object without prose.','prompt':prompt,'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest()})
            gold.append({'request_id':rid,'case_id':c['case_id'],'condition':name,'weights':dict(zip(ASSETS,w)),'volatility_pct':risk(w,c['returns_pct'])})
    return requests,gold


def validate(cases,requests,gold):
    max_error=0.;checks=0;cov_error=0.;profiles=set()
    for c in cases:
        w=c['base_weights'];R=c['returns_pct']
        key=json.dumps([R,w]);assert key not in profiles;profiles.add(key)
        for form in ['one','eight','matched_one','matched_eight','heterogeneous','canonical']:
            g=graph(w,form);actual=[sum(q*v[k] for q,v in g) for k in range(2)]
            for r in R:
                d=abs(sum(v*x for v,x in zip(actual,r))-sum(v*x for v,x in zip(w,r)))
                max_error=max(max_error,d);assert d<1e-10
            checks+=1
        for w in [c['base_weights'],c['control_weights']]:
            mean=[sum(r[j] for r in R)/8 for j in range(2)]
            cov=[[sum((r[j]-mean[j])*(r[k]-mean[k]) for r in R)/8 for k in range(2)] for j in range(2)]
            sig=math.sqrt(sum(w[j]*w[k]*cov[j][k] for j in range(2) for k in range(2)))
            cov_error=max(cov_error,abs(sig-risk(w,R)));assert abs(sig-risk(w,R))<1e-10
    assert len({x['request_id'] for x in requests})==len(requests)==len(gold)
    text={(p['case_id'],p['condition']):p['prompt'] for p in requests}
    word_matches=0
    for c in cases:
        a=text[(c['case_id'],'matched_one')];b=text[(c['case_id'],'matched_eight')]
        assert len(a.split())==len(b.split());word_matches+=1
    eval_cases=[c for c in cases if c['split']=='evaluation']
    return {'status':'STIMULUS_VALIDATION_ONLY','base_records':len(cases),'unique_profiles':len(profiles),'prompts':len(requests),'evaluation_cases':len(eval_cases),'evaluation_prompts':sum(p['split']=='evaluation' for p in requests),'graph_checks':checks,'max_payoff_error_pct':max_error,'alternative_covariance_checks':2*len(cases),'max_covariance_error_pct':cov_error,'matched_word_count_pairs':word_matches,'control_increases':sum(c['control_direction']=='increase' for c in cases),'control_decreases':sum(c['control_direction']=='decrease' for c in cases),'model_responses_at_freeze':0}


def main():
    DATA.mkdir(parents=True,exist_ok=True)
    if (ROOT/'results/raw_responses.jsonl').exists():
        raise RuntimeError('Refusing to overwrite frozen stimuli after inference started')
    cases=make_cases();requests,gold=make_prompts(cases)
    report=validate(cases,requests,gold)
    write_jsonl(DATA/'cases.jsonl',cases);write_jsonl(DATA/'prompts.jsonl',requests);write_jsonl(DATA/'answer_key.jsonl',gold)
    (DATA/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    manifest={'frozen_at_utc':datetime.now(timezone.utc).isoformat(),'status':'EXPLORATORY_PROTOCOL_FROZEN_BEFORE_MODEL_RESPONSES_NOT_EXTERNALLY_PREREGISTERED','model_id':MODEL,'model_revision':REVISION,'quantization':'Q4_K_M','engine':'llama.cpp b12110 CPU','temperature':0,'seed':20261104,'max_tokens':128,'replicates':1,'evaluation_split_only':True,'request_order_seed':20261104,'source_url':SOURCE_URL,'source_sha256':sha(ROOT/'data/source/49_Industry_Portfolios_CSV.zip'),'files':{p.name:sha(p) for p in sorted(DATA.glob('*.jsonl'))},'analysis_plan':{'primary':'mean normalized direct_eight minus direct_one, separately by domain','controls':'matched-one/eight, verified weights, canonical input, extraction plus fixed calculator, heterogeneous products, balanced increases/decreases','accuracy_thresholds_relative':[.01,.05],'exposure_l1_tolerance':1e-6,'bootstrap':'case paired, 10000 samples, exploratory 95% percentile intervals','failures':'retain all raw outputs; invalid outputs excluded only from numerical conditional means; report coverage and failed attempts','claim_limit':'one small quantized model, no general LLM, causal mechanism, market forecasting, or publication-readiness claim'}}
    (DATA/'protocol.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
