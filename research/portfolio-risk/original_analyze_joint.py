"""Observed declared-exposure/risk decomposition, without hidden-state claims."""
import json,math
from pathlib import Path
from build_experiment import ROOT,DATA,load_jsonl,risk,sha
from analyze_experiment import parse,number


def analyze(folder,response_file=None,output_dir=None):
    folder=Path(folder);raw=load_jsonl(response_file if response_file else folder/'raw_responses.jsonl')
    dest=Path(output_dir) if output_dir else folder;dest.mkdir(parents=True,exist_ok=True)
    cases={c['case_id']:c for c in load_jsonl(DATA/'cases.jsonl')}
    prompts={p['request_id']:p for p in load_jsonl(DATA/'joint_prompts.jsonl')}
    records=[]
    for r in raw:
        p=prompts[r['request_id']];c=cases[p['case_id']]
        w,status=parse(r.get('raw_text'),'extract');v,status_v=parse(r.get('raw_text'),'risk')
        good=w is not None and v is not None
        row={'request_id':r['request_id'],'case_id':c['case_id'],'domain':c['domain'],'condition':p['condition'],'valid_joint':good,'weights_status':status,'risk_status':status_v}
        if good:
            true=risk(c['base_weights'],c['returns_pct']);declared=risk(w,c['returns_pct'])
            row.update({'reported_weights':w,'reported_risk_pct':v,'true_risk_pct':true,'risk_of_reported_weights_pct':declared,'exposure_l1_error':sum(abs(a-b) for a,b in zip(w,c['base_weights'])),'normalized_total_error':(v-true)/true,'normalized_reported_exposure_component':(declared-true)/true,'normalized_inconsistency_component':(v-declared)/true})
            assert abs(row['normalized_total_error']-row['normalized_reported_exposure_component']-row['normalized_inconsistency_component'])<1e-10
        records.append(row)
    valid=[r for r in records if r['valid_joint']];correct=[r for r in valid if r['exposure_l1_error']<=1e-6]
    out={'status':'OBSERVED_JOINT_OUTPUT_DIAGNOSTIC','model_id':raw[0]['model_id'],'attempts':len(raw),'valid_joint':len(valid),'correct_reported_exposures':len(correct),'risk_within_5pct_given_correct_reported_exposures':sum(abs(r['normalized_total_error'])<=.05 for r in correct),'inconsistent_with_own_weights_by_over_5pct_of_true_risk':sum(abs(r['normalized_inconsistency_component'])>.05 for r in valid),'raw_sha256':sha(folder/'raw_responses.jsonl'),'interpretation':'Reported weights are observable outputs, not evidence of the model hidden reasoning process.','records':records}
    out['posthoc_output_normalization']=response_file is not None
    (dest/'analysis.json').write_text(json.dumps(out,indent=2)+'\n');return out


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('folder');a=p.parse_args();r=analyze(a.folder)
    print(json.dumps({k:v for k,v in r.items() if k!='records'},indent=2))
