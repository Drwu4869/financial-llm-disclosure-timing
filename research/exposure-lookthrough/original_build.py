"""Freeze a fresh, controlled follow-up before collecting any model responses."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import random,json,hashlib
ROOT=Path(__file__).resolve().parent
SEED=2026110506

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write_jsonl(p,rs):p.write_text(''.join(json.dumps(r,sort_keys=True)+'\n' for r in rs))
def gold(rows):return sum(F(r['amount_gbp'])*F(r['a_percent']) for r in rows)/sum(F(r['amount_gbp']) for r in rows)
def make_rows(q,b,split):
    rs=[]
    for j in range(4):
        parts=[q[j]*100] if j!=split else [q[j]*20,q[j]*30,q[j]*50]
        for amount in parts:
            rs.append({'lot':len(rs)+1,'product':j+1,'amount_gbp':amount,'a_percent':b[j]})
    return rs

def main():
    data=ROOT/'data';data.mkdir(exist_ok=True)
    if (data/'protocol.json').exists():raise SystemExit('Already frozen; do not replace an existing protocol.')
    rng=random.Random(SEED);cases=[];prompts=[]
    for i in range(24):
        q=list(rng.choice([[10,20,30,40],[15,20,25,40],[5,15,35,45],[10,15,30,45]]));rng.shuffle(q)
        c=rng.choice([x for x in range(31,70) if x!=50])
        for attempt in range(100000):
            d=[rng.randint(-30,30) for _ in range(3)]
            tail=-sum(q[j]*d[j] for j in range(3))
            if tail%q[3]:continue
            d.append(tail//q[3]);b=[c+x for x in d]
            if min(b)>=5 and max(b)<=95 and len(set(b))==4 and abs(sum(d)/4)>=5:break
        else:raise RuntimeError('Could not generate matched family')
        split=i%4
        case={'family':f'new_{i:02d}','q_percent':q,'homogeneous_b_percent':[c]*4,'heterogeneous_b_percent':b,'gold_percent':c,'split_product':split+1}
        cases.append(case)
        conditions=[]
        for structure,bs in [('homogeneous',[c]*4),('heterogeneous',b)]:
            for representation in ['merged','fragmented']:
                conditions.append((structure,representation,make_rows(q,bs,split if representation=='fragmented' else -1),['direct','ledger']))
        changed=q.copy();lo=b.index(min(b));hi=b.index(max(b));changed[lo]-=5;changed[hi]+=5
        # Zero allocation is allowed only in this genuine-change control; omit it.
        cr=[r for r in make_rows(changed,b,-1) if r['amount_gbp']>0]
        for j,r in enumerate(cr):r['lot']=j+1
        assert gold(cr)-c>=1
        conditions.append(('changed','merged',cr,['direct']))
        for structure,representation,rows,methods in conditions:
            lead='This account contains only Asset A and Asset B through the products listed below. Each lot is separately funded. Count every lot, including repeated products. Product allocations are percentages of that product; all remaining assets are B. There are no fees, leverage or cash balances.\n'
            body='\n'.join(f"Lot {r['lot']}: GBP {r['amount_gbp']} invested in Product {r['product']}; Asset A is {r['a_percent']}% of this product and Asset B is {100-r['a_percent']}%." for r in rows)
            for method in methods:
                task='\nWhat percentage of the entire account is exposed to Asset A? '
                if method=='direct':task+='Return only JSON with the numeric key total_a_percent. Use percentage points on the 0 to 100 scale.'
                else:task+='First report each lot as [lot_number, amount_in_GBP, A_percentage_of_that_product], then give the account total. Return only JSON with rows (an array of those three-number arrays) and total_a_percent (a number). Keep the original lot numbers and list each lot exactly once. All percentages use the 0 to 100 scale.'
                rid=f"{case['family']}_{structure}_{representation}_{method}"
                prompts.append({'request_id':rid,'family':case['family'],'structure':structure,'representation':representation,'method':method,'system':'Read the supplied account and return the requested JSON.','prompt':lead+body+task,'gold_percent_exact':str(gold(rows)),'gold_rows':rows})
    write_jsonl(data/'cases.jsonl',cases);write_jsonl(data/'prompts.jsonl',prompts)
    protocol={'created_at_utc':datetime.now(timezone.utc).isoformat(),'stage':'fresh prospective follow-up after v5; local timestamp, not external preregistration','seed':SEED,'families':24,'requests_per_model':216,'observations_per_family':9,'independent_unit':'generated portfolio family, not prompt','provenance':'All inputs are synthetic controlled accounts. They are not issuer documents, customer portfolios, or model answers. No LLM generated gold labels.','primary':'Paired homogeneous-minus-heterogeneous direct accuracy, averaging merged and fragmented forms within family.','secondary':['correct total with incorrect ledger in the same response','ledger+calculator minus direct accuracy','fragmented-minus-merged absolute error','response to genuine exposure change'],'accuracy_tolerance_percentage_points':0.5,'ledger_tolerances':{'amount_gbp':0.005,'a_percentage_points':0.00005},'bootstrap':{'replicates':10000,'seed':2026110507,'unit':'family','interval':'percentile 95%; exploratory with 24 generated families'},'parsing':'Strict JSON numbers, finite and within stated units. Do not rescale percentages, renormalize, discard wrong outputs or repair JSON. Missing/duplicate lots invalidate ledger calculator.','model_plan':'Run available Qwen3-8B Q4_K_M non-thinking first. Stronger-model confirmation is pending external execution access. No claim about stronger models is licensed.','stopping':'Collect all 216 requests for each declared model. No stopping on accuracy. Infrastructure interruptions may resume only unsaved requests; recorded responses/errors are retained.','inference':{'temperature':0,'seed':SEED,'max_tokens':512,'json_object':True,'reasoning':'off'},'success_interpretation':'The primary accuracy gap is a task-diagnostic comparison, not a causal measurement of internal shortcut reasoning. Null or reversed gaps will be reported.','files':{}}
    for name in ['cases.jsonl','prompts.jsonl']:protocol['files']['data/'+name]=digest(data/name)
    for name in ['build.py','score.py','analyze.py','run_local.py','test_experiment.py']:protocol['files'][name]=digest(ROOT/name)
    (data/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    print(json.dumps({'families':len(cases),'requests':len(prompts),'protocol_sha256':digest(data/'protocol.json')}))
if __name__=='__main__':main()
