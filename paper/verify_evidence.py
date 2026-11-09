"""Recheck paper counts and SEC metadata, without executing model-generated code.

Run after extracting the complete reproducibility archive. This script reads
the two sibling directories disclosure_code_pilot/ and rule_history/.
"""
from pathlib import Path
import collections
import csv
import datetime as dt
import hashlib
import json
import statistics as st

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
PILOT=BASE/'disclosure_code_pilot'
A04=PILOT/'extensions/A04_form_swap'
SEC=BASE/'rule_history'
def read(path): return json.loads(path.read_text())

def metadata():
    manifest=read(SEC/'data/download_manifest.json')
    assert len(manifest)==28
    for entry in manifest:
        assert hashlib.sha256((SEC/entry['path']).read_bytes()).hexdigest()==entry['sha256']
    seen=set(); rows=[]; exclusions=collections.Counter()
    for path in sorted((SEC/'data').glob('*/SUBMISSION.tsv')):
        with path.open(encoding='utf-8-sig',newline='') as stream:
            for row in csv.DictReader(stream,delimiter='\t'):
                acc=row['ACCESSION_NUMBER']; assert acc and acc not in seen; seen.add(acc)
                if row['SUB_TYPE']!='NPORT-P':
                    exclusions['amendment']+=1; continue
                filing,report,ending=[dt.datetime.strptime(row[k],'%d-%b-%Y').date()
                    for k in ('FILING_DATE','REPORT_DATE','REPORT_ENDING_PERIOD')]
                if (ending.month-report.month)%3:
                    exclusions['off_fiscal_quarter_month']+=1; continue
                assert filing>=report>=dt.date(2019,9,30)
                lag=(filing-report).days
                rows.append(dict(accession=acc,report_date=str(report),lag_days=lag,wait_days=max(0,60-lag)))
    with (SEC/'results/eligible_accessions.tsv').open(newline='') as stream:
        old={r['accession']:r for r in csv.DictReader(stream,delimiter='\t')}
    assert len(seen)==355115 and len(rows)==len(old)==349673
    for row in rows:
        assert all(row[k]==int(old[row['accession']][k]) for k in ('lag_days','wait_days'))
    def stats(rr):
        waits=[r['wait_days'] for r in rr];lags=[r['lag_days'] for r in rr];n=len(rr)
        return dict(n=n,median_lag=st.median(lags),mean_wait=st.mean(waits),median_wait=st.median(waits),
          positive_count=sum(w>0 for w in waits),positive_percent=100*sum(w>0 for w in waits)/n,
          at_least5_percent=100*sum(w>=5 for w in waits)/n,after60_count=sum(l>60 for l in lags),
          bins={label:sum(lo<=w<=hi for w in waits) for label,lo,hi in
            [('0',0,0),('1-2',1,2),('3-4',3,4),('5-9',5,9),('10-19',10,19),('20+',20,1000)]})
    result=dict(verified_raw_tables=28,raw_rows=len(seen),excluded=dict(exclusions),
       full_cohort=stats(rows),report_2022_2023_posthoc=stats([r for r in rows if '2022-01-01'<=r['report_date']<'2024-01-01']),
       checked_against_prior_rows=True,prior_summary_sha256=hashlib.sha256((SEC/'results/summary.json').read_bytes()).hexdigest())
    assert result==read(ROOT/'evidence/metadata_recheck.json')
    return result

def models():
    pilot=read(PILOT/'results/full_horizon/rule_classification.json')['programs']
    counts=collections.Counter(r['category'] for r in pilot)
    assert counts=={'oracle_alignment':24,'sixty_day_floor':10,'filing_date_strict':1,'interface_refusal':1}
    for cond in ['P0','P1']:
        rr=[r for r in pilot if r['token'].startswith('GPT_') and '_'+cond+'_' in r['token']]
        assert len(rr)==6 and sum(r['category']=='sixty_day_floor' for r in rr)==5
    summary=read(A04/'SUMMARY.json')
    assert summary==read(ROOT/'evidence/A04_SUMMARY.json')
    assert summary['evaluated']==summary['returned']==36
    programs=[]
    for path in sorted((A04/'results').glob('*.json')):
        if path.name.startswith(('GPT_','CLAUDE_')):
            programs.append(read(path))
    assert len(programs)==36
    for cell in summary['cells']:
        prefix='_'.join([cell['vendor'],cell['form'],cell['condition']])+'_'
        rr=[r for r in programs if r['token'].startswith(prefix)]
        assert len(rr)==3
        counts={k:sum(k in r['matching_policy_all_seeds'] for r in rr) for k in cell['all_seed_policy_counts']}
        assert counts==cell['all_seed_policy_counts']
        assert all(r['valid_portfolio_seeds']==5 and not r['has_witness'] for r in rr)
    for vendor in ['GPT','CLAUDE']:
        rr=[r for r in programs if r['token'].startswith(vendor+'_F13_') and '_P2_' not in r['token']]
        assert len(rr)==6 and all(not any(p.startswith('floor45') for p in r['matching_policy_all_seeds']) for r in rr)
        rr=[r for r in programs if r['token'].startswith(vendor+'_') and '_P2_' in r['token']]
        assert len(rr)==6 and all('filing_inclusive' in r['matching_policy_all_seeds'] for r in rr)
    ex=read(A04/'EXPLORATORY_CALENDAR.json')
    assert sum(r['new_explanation_only'] for r in ex['programs'])==2
    audit=read(A04/'SAVED_AUDIT.json')
    assert audit['baseline_daily_vectors']==85860
    assert audit['intervention_outcomes']=={'inconclusive_intervention_refusal':65,'no_witness':2095}
    return dict(pilot_dated_programs=len(pilot),A04_programs=len(programs),A04_baseline_vectors=85860,
       A04_no_witness=2095,A04_inconclusive=65,posthoc_calendar_matches=2)

if __name__=='__main__':
    result={'models':models(),'metadata':metadata(),'candidate_programs_executed':False}
    (ROOT/'evidence/manuscript_verification.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'status':'passed',**result['models'],
      'SEC_accessions':result['metadata']['full_cohort']['n'],
      'SEC_historical_subset':result['metadata']['report_2022_2023_posthoc']['n']}))
