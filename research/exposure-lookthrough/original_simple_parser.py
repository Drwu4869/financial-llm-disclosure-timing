"""Format-specific deterministic baseline, not a general document reader."""
from fractions import Fraction as F
import re,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def solve(text):
    target=re.search(r'^Target underlying fund \(Asset A\): (.+)$',text,re.M).group(1)
    blocks=re.split(r'\nFund ([A-Z0-9]+): ',text)[1:]
    weights={}
    for fund,body in zip(blocks[::2],blocks[1::2]):
        pairs=re.findall(r'^(.+) \| ([\d.]+)%$',body,re.M)
        found=[F(v) for name,v in pairs if name==target]
        if not found:
            assert 'a target absent from a table contributes zero' in text
            weights[fund]=F(0)
        else:
            assert len(found)==1;weights[fund]=found[0]
    lots=re.findall(r'^Lot (\d+): GBP (\d+) invested in Fund ([A-Z0-9]+)\.$',text,re.M)
    assert lots and weights
    rows=[[int(i),int(m),weights[f]] for i,m,f in lots]
    return rows,sum(m*w for _,m,w in rows)/sum(m for _,m,_ in rows)

if __name__=='__main__':
    ps=[json.loads(l) for l in (ROOT/'data/source_prompts.jsonl').read_text().splitlines()]
    results=[]
    for p in ps:
        rows,value=solve(p['prompt'])
        results.append({'request_id':p['request_id'],'answer_exact':value==F(p['gold_percent_exact']),'computed_percent_exact':str(value),'rows_exact':all((i,m,w)==(r['lot'],r['amount_gbp'],F(r['a_percent'])) for (i,m,w),r in zip(rows,p['gold_rows']))})
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/simple_parser.json').write_text(json.dumps({'scope':'Exact matching and regular expressions tailored to the standardized source-table prompt format. Not a general PDF/text baseline; no model inference.','n':len(results),'exact_totals':sum(r['answer_exact'] for r in results),'exact_rows':sum(r['rows_exact'] for r in results),'results':results},indent=2)+'\n')
    print(sum(r['answer_exact'] for r in results),'/',len(results),'exact parser totals')
