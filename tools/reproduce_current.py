"""Extract the public evidence bundle and run authored saved-evidence checks.

Does not request models, import generated source, or run candidate programs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True,help='New or empty extraction directory (about 650 MB)')
    args=parser.parse_args()
    out=args.output.resolve()
    if out.exists() and any(out.iterdir()):parser.error('Output must be new or empty; existing evidence will not be overwritten')
    archive=ROOT/'archive/packages/Disclosure_Timing_Public_Evidence.zip'
    manifest=json.loads((ROOT/'release_manifest.json').read_text())
    expected=next(x['sha256'] for x in manifest['files'] if x['path']==str(archive.relative_to(ROOT)))
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=expected:raise AssertionError('Evidence archive hash mismatch')
    out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            dest=(out/info.filename).resolve()
            if not dest.is_relative_to(out):raise ValueError('Unsafe archive path')
            if ((info.external_attr>>16)&0o170000)==0o120000:raise ValueError('Archive symlink')
        z.extractall(out)
    for script in ['verify_evidence.py','revision_checks.py']:
        print('Running authored saved-evidence check:',script,flush=True)
        subprocess.run([sys.executable,script],cwd=out/'submission_paper',check=True)
    print(json.dumps({'status':'passed','output':str(out),'model_calls':0,
        'candidate_programs_executed':False,'checks':['verify_evidence.py','revision_checks.py']}))

if __name__=='__main__':main()
