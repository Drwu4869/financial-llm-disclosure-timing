"""Recheck archived historical evidence; no model requests or candidate-code execution.

Requires NumPy and SciPy for the original analysis and bound checker.
Run from any directory. Temporary extraction never overwrites the source archives.
The original verification/scoring scripts are invoked in their original layout.
"""
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from io import BytesIO
from hashlib import sha256
from datetime import datetime, timezone
from fractions import Fraction as F
import argparse
import json
import stat
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def safe_extract(archive, destination):
    destination.mkdir(parents=True, exist_ok=True)
    for item in archive.infolist():
        name=PurePosixPath(item.filename)
        if name.is_absolute() or '..' in name.parts or stat.S_ISLNK(item.external_attr >> 16):
            raise ValueError('Unsafe archive entry: '+item.filename)
    archive.extractall(destination)

def run_script(work, script):
    p=subprocess.run([sys.executable, script],cwd=work,capture_output=True,text=True,timeout=180)
    if p.returncode:
        raise RuntimeError(script+' failed:\n'+(p.stdout+p.stderr)[-4000:])
    return p.stdout.strip()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,help='Optional destination outside the frozen research materials')
    args=parser.parse_args()
    mapping=json.loads((ROOT/'research/source-map.json').read_text())
    cache={}
    def get_archive(path, chain=()):
        key=(path,tuple(chain))
        if key not in cache:
            if chain:
                parent=get_archive(path,chain[:-1]);cache[key]=ZipFile(BytesIO(parent.read(chain[-1])))
            else:cache[key]=ZipFile(ROOT/path)
        return cache[key]
    for row in mapping['files']:
        expected=get_archive(row['archive'],row['nested_archives']).read(row['member'])
        actual=(ROOT/row['path']).read_bytes()
        assert actual==expected, row['path']
        assert len(actual)==row['bytes'] and sha256(actual).hexdigest()==row['sha256'], row['path']
    checks={}
    with TemporaryDirectory(prefix='portfolio-history-') as td:
        work=Path(td)
        a=get_archive('archive/packages/Portfolio_Risk_LaTeX_and_Evidence_v5.zip')
        safe_extract(a,work/'v5')
        checks['exact_certificate_provenance']=json.loads(run_script(work/'v5','experiment_v4/verify_certificates.py'))
        b=get_archive('archive/packages/Portfolio_Exposure_v9_LaTeX_and_Evidence.zip',[
            'Portfolio_Exposure_v9/evidence/Portfolio_Risk_Integrated_v8.zip',
            'Portfolio_Risk_Integrated_v8/evidence/Portfolio_Exposure_Validation_v7.zip'])
        safe_extract(b,work/'v7')
        base=work/'v7/Portfolio_Exposure_Validation_v7'
        checks['controlled_request_binding']=json.loads(run_script(base/'controlled','audit.py'))
        checks['exposure_study_request_binding']=json.loads(run_script(base,'audit_release.py'))
        assert sum(x['requests'] for x in checks['exposure_study_request_binding']['sets'])==536
        r=get_archive('archive/packages/Portfolio_Risk_Thinking_Recheck.zip')
        safe_extract(r,work/'recheck');recheck=work/'recheck/thinking_recheck'
        expected=json.loads((recheck/'results/analysis.json').read_text())
        checks['recheck_provenance']=json.loads(run_script(recheck,'verify_record_provenance.py'))
        run_script(recheck,'analyze.py')
        actual=json.loads((recheck/'results/analysis.json').read_text())
        assert expected==actual, 'Recheck analysis differs from saved result'
        groups=['controlled_homogeneous','controlled_heterogeneous','source_direct','source_ledger']
        rows={v['configuration']:v['groups'] for v in actual['summaries'] if v['view']=='strict'}
        counts=[[rows[c][g]['answer_correct'] for g in groups] for c in ['original','thinking']]
        assert counts==[[24,4,2,5],[24,24,25,25]]
        checks['recheck_analysis']={'matches_saved_analysis':True,'counts':counts,'total_correct':[sum(v) for v in counts],
                                    'new_responses':actual['evaluation_calls'],'truncated':actual['truncated']}
        top=get_archive('archive/packages/Top10_Disclosure_Pilot_20.zip')
        safe_extract(top,work/'top10')
        checks['top10_answer_key']=run_script(work/'top10/Top10_Disclosure_Pilot','verify.py')
    # Arithmetic used by the retrospective explanations, not new empirical results.
    q=[F(1,4),F(3,4)];hom=[F(3,5)]*2;het=[F(3,10),F(7,10)]
    rules=[q,[F(1,2)]*2,[F(0),F(1)],[F(2,5),F(3,5)]]
    assert [sum(x*y for x,y in zip(p,hom)) for p in rules]==[F(3,5)]*4
    assert [sum(x*y for x,y in zip(p,het)) for p in rules]==[F(3,5),F(1,2),F(7,10),F(27,50)]
    assert F(6900)*F('14.8')/10000==F('10.212')
    assert F('.4')*5==2 and F('.4')*5+F('.6')*F('3.2')==F('3.92')
    report={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS',
            'browsable_source_copies':len(mapping['files']),'copies_match_archives':True,
            'checks':checks,'worked_example_arithmetic':'PASS','new_model_calls':0,
            'candidate_programs_executed':False,
            'scope':'Selected saved-evidence checks, not a rerun of every historical experiment or independent human replication. Public export archive bytes differ from original private release containers; each copied member is checked against its published container.'}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
