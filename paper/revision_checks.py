"""Post-hoc manuscript audit: fixture sensitivity, realized lags and quotations.

Runs authored reference policies only. It never executes candidate programs.
"""
import ast
import datetime as dt
import hashlib
import gzip
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
A04=BASE/'disclosure_code_pilot/extensions/A04_form_swap'
QA=BASE/'rule_history/model_run_v1'
sys.path.insert(0,str(A04))
from study import policy, SEEDS, assigned_filing_date, next_edgar, add_days

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    frozen=read(A04/'FREEZE.json')
    for name,digest in frozen['files'].items():assert sha(A04/name)==digest
    cases=[];lag_union=set()
    for seed in SEEDS:
        f=read(A04/'fixtures'/f'{seed}.json');p=f['payload']
        periods=sorted({(r['period_end'],r['filing_date']) for r in p['filings']})
        lags=[(dt.date.fromisoformat(a)-dt.date.fromisoformat(r)).days for r,a in periods]
        lag_union.update(lags)
        def compare(left,right):
            a,b=policy(p,left),policy(p,right)
            per_day=[max(abs(x-y) for x,y in zip(wa,wb)) for wa,wb in zip(a,b)]
            return {'changed_days':sum(e>1e-8 for e in per_day),'max_error':max(per_day),
                    'dates':[day for day,error in zip(p['dates'],per_day) if error>1e-8]}
        inc=compare('filing_inclusive','floor45_inclusive')
        strict=compare('filing_strict','floor45_strict')
        assert inc['changed_days']>0 and strict['changed_days']>0
        # Independently reimplement selection and normalization; do not reuse
        # engine.normalize or study.policy in this cross-check.
        def independent(strict=False,floor=False):
            result=[]
            for day in p['dates']:
                values=[]
                for asset in p['assets']:
                    eligible=[]
                    for row in p['filings']:
                        if row['asset']!=asset:continue
                        public=dt.date.fromisoformat(row['filing_date'])
                        if floor:public=max(public,dt.date.fromisoformat(row['period_end'])+dt.timedelta(days=45))
                        cut=dt.date.fromisoformat(day)
                        if public<cut or (public==cut and not strict):eligible.append(row)
                    row=max(eligible,key=lambda r:r['period_end']) if eligible else None
                    values.append(row['weight_pct'] if row else 100/len(p['assets']))
                avg=sum(values)/len(values);v=[x-avg for x in values];den=sum(abs(x) for x in v)
                result.append([x/den for x in v] if den else [0.0]*len(v))
            return result
        for s in [False,True]:
            for fl in [False,True]:
                name=('floor45' if fl else 'filing')+('_strict' if s else '_inclusive')
                assert max(abs(x-y) for wa,wb in zip(independent(s,fl),policy(p,name)) for x,y in zip(wa,wb))<=1e-8
        cases.append({'seed':seed,'decision_days':len(p['dates']),
            'periods':[r for r,a in periods],'assigned_lags_days':lags,
            'inclusive_comparison':inc,'strict_comparison':strict,'fixture_sha256':sha(A04/'fixtures'/f'{seed}.json')})
    assert sorted(lag_union)==[12,13,25,26,40,41,46,47,61,62]
    assert [c['inclusive_comparison']['changed_days'] for c in cases]==[40,25,41,39,39]
    assert [c['strict_comparison']['changed_days'] for c in cases]==[39,24,40,39,38]
    quotes=[
      ('CLAUDE_NPORT_P1_r2','under the 2022-2023 N-PORT regime the public third-fiscal-month portion is released 60 days after fiscal-quarter end even if filed earlier'),
      ('GPT_NPORT_P0_r1','For 2022-2023 third-fiscal-month Form N-PORT reports, public availability is no earlier than 60 calendar days after period_end.')]
    quoted=[]
    for token,quote in quotes:
        path=A04/'responses'/f'{token}.py';code=path.read_text()
        strings=[' '.join(n.value.split()) for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
        assert any(quote in text for text in strings),(token,quote)
        quoted.append({'token':token,'quote':quote,'source_sha256':sha(path),
                       'source_path':str(path.relative_to(BASE)),'verification':'Contiguous AST string content after whitespace normalization; source not executed.'})
    # Opening example: verify a saved execution, then independently calculate
    # row eligibility. This is not a new candidate run or a new model answer.
    lead_id='CLAUDE_NPORT_P0_r1'
    lead_results=read(A04/'results'/f'{lead_id}.json')
    lead_seed=next(r for r in lead_results['seeds'] if r['seed']==101)
    lead_path=A04/'results'/lead_seed['outputs_file']
    assert sha(lead_path)==lead_seed['outputs_sha256']
    with gzip.open(lead_path,'rt') as stream:lead_saved=json.load(stream)
    lead_reason=lead_saved[0]['reason']
    assert lead_reason==lead_seed['reason']
    for excerpt in ['40 of 48 rows became usable after their filing_date',
                    'released 60 days after quarter end even when filed earlier']:
        assert excerpt in lead_reason
    lead_payload=read(A04/'fixtures/101.json')['payload']
    lead_rows=[]
    for row in lead_payload['filings']:
        available=next_edgar(max(row['filing_date'],add_days(row['period_end'],60)))
        lead_rows.append({'row_id':row['row_id'],'period_end':row['period_end'],
                         'filing_date':row['filing_date'],'calendar_floor_available':available,
                         'delayed':available>row['filing_date']})
    assert len(lead_rows)==48 and sum(r['delayed'] for r in lead_rows)==40
    delayed_periods=sorted({r['period_end'] for r in lead_rows if r['delayed']})
    unchanged_periods=sorted({r['period_end'] for r in lead_rows if not r['delayed']})
    assert len(delayed_periods)==5 and len(unchanged_periods)==1
    assert set(delayed_periods).isdisjoint(unchanged_periods)
    for period in delayed_periods:
        assert sum(r['period_end']==period and r['delayed'] for r in lead_rows)==8
    unchanged_rows=[r for r in lead_rows if not r['delayed']]
    assert len(unchanged_rows)==8
    assert all((dt.date.fromisoformat(r['filing_date'])-dt.date.fromisoformat(r['period_end'])).days==61 for r in unchanged_rows)

    lead={'token':lead_id,'seed':101,'reason':lead_reason,'saved_outputs_sha256':sha(lead_path),
          'total_rows':48,'delayed_rows':40,'delayed_periods':delayed_periods,
          'unchanged_periods':unchanged_periods,'rows':lead_rows,
          'scope':'Forty rows delayed in five of six report periods; eight rows in the day-61 period unchanged; not simultaneous withholding on one day; post-hoc saved-output audit.'}
    dec=[r for r in read(QA/'direct_decodes.json') if r['model']=='GPT-6 High']
    app=[r for r in read(QA/'application_grades.json') if r['model']=='GPT-6 High']
    summ=read(BASE/'rule_history/results/model_run_summary.json')['models']['GPT-6 High']
    assert len(dec)==17 and len(app)==27
    panel={r['id']:r for r in read(BASE/'rule_history/plan/panel_with_gold.json')['items']}
    failures=[r for r in app if not r['core_correct']];assert [r['id'] for r in failures]==['P42']
    assert summ['direct']['core_correct']==15 and summ['application']['core_correct']==16
    assert summ['oracle']['core_correct']==9 and summ['diagnostic']['core_correct']==1
    assert {panel[r['id']]['family'] for r in dec if r['id'] in ['P02','P41']}=={'NPORT'}
    qa={'setting':'GPT-6 High; preceding 7 November 2026 panel; contextual evidence only',
        'direct':{'correct':15,'total':17,'incorrect_ids':['P02','P41']},
        'application':{'correct':16,'total':17,'incorrect_ids':['P42']},
        'rule_provided':{'correct':9,'total':9},'deadline_diagnostic':{'correct':1,'total':1},
        'NPORT_release_anchor':[]}
    for pid in ['P02','P41','P42','P43','P44']:
        path=QA/f'GPT_{pid}.txt';qa['NPORT_release_anchor'].append({'id':pid,'prompt':panel[pid]['prompt'],
            'reference':panel[pid]['gold'],'response':path.read_text(),'sha256':sha(path)})
    result={'dated':'2026-11-09','designation':'Post-hoc manuscript diagnostics; no new model answers, no changed frozen scores',
       'candidate_programs_executed':False,'tolerance':1e-8,'realized_lag_union_days':sorted(lag_union),
       '45_day_floor_sensitivity':cases,'quotes':quoted,'preceding_QA':qa,'opening_case':lead}
    (ROOT/'evidence/revision_checks_2026-11-09.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'status':'passed','realized_lags':sorted(lag_union),'inclusive_changed_days':[c['inclusive_comparison']['changed_days'] for c in cases],
      'strict_changed_days':[c['strict_comparison']['changed_days'] for c in cases],'verified_quotes':len(quoted),
      'GPT_QA_direct':'15/17','GPT_QA_application':'16/17','opening_case_delayed_rows':'40/48','opening_case_delayed_periods':'5/6'}))

if __name__=='__main__':main()
