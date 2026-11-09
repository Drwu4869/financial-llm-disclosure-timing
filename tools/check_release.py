"""Verify distributed bytes and the central saved-evidence counts; stdlib only."""
from pathlib import Path
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parents[1]

def main():
    manifest=json.loads((ROOT/'release_manifest.json').read_text())
    for row in manifest['files']:
        p=ROOT/row['path']
        if not p.is_file():raise AssertionError('Missing file: '+row['path'])
        b=p.read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:
            raise AssertionError('Changed file: '+row['path'])
    evidence=json.loads((ROOT/'evidence/manuscript_verification.json').read_text())
    assert evidence['candidate_programs_executed'] is False
    cohort=evidence['metadata']['full_cohort']
    assert cohort['n']==349673 and cohort['positive_count']==300464
    assert abs(cohort['mean_wait']-4.126046334718437)<1e-12
    assert evidence['models']['A04_programs']==36
    assert evidence['models']['A04_no_witness']==2095
    assert evidence['models']['A04_inconclusive']==65
    programs=json.loads((ROOT/'evidence/discovery_program_rules.json').read_text())['programs']
    selected=[p for p in programs if p['token'].startswith('GPT_') and any('_'+c+'_' in p['token'] for c in ['P0','P1'])]
    assert len(selected)==12 and sum(p['category']=='sixty_day_floor' for p in selected)==10
    print(json.dumps({'status':'passed','files_verified':len(manifest['files']),
        'discovery_floor':'10/12','followup_programs':36,'eligible_accessions':349673,
        'model_calls':0,'candidate_programs_executed':False}))

if __name__=='__main__':main()
