"""Check the frozen materials, score the recorded answers and reconstruct the key."""
import csv
import hashlib
import json
import re
from decimal import Decimal as D
from pathlib import Path
base=Path(__file__).resolve().parent.parent
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
key=read(base/'scoring/key.json')
protocol=read(base/'protocol.json')
assert sha(base/'scoring/key.json')==protocol['key_sha256']
assert all(sha(base/'inputs'/k)==v for k,v in protocol['input_text_sha256'].items())
weights=[D('.4'),D('.6')]
annual=(base/'inputs/BlackRock_Investment_Funds_Annual_Report_2025.txt').read_text()
historical=[D(x) for x in re.findall(r'^iShares USD Treasury Bond 3-7yr UCITS ETF \| ([\d.]+)$',annual,re.M)]
def value(xs):return sum(w*x for w,x in zip(weights,xs))
assert value(historical)==D(key['A']['lo'])==D(key['A']['hi'])
facts=[]
for num in [3,5]:
    text=(base/'inputs'/f'MyMap_{num}_Select_ESG.txt').read_text()
    rows=dict((n,D(v)) for n,v in re.findall(r'^(.+?) \| (\d+\.\d+)%$',text,re.M) if n!='Total of Portfolio')
    assert len(rows)==10 and list(rows.values())==sorted(rows.values(),reverse=True)
    facts.append(rows)
short='ISHS $ TRSY BOND 3-7 YR UCITS ETF'
long='ISHS $ TSY BOND 7-10YR UCITS ETF'
assert short not in facts[1]
lo=value([facts[0][short],D(0)])
hi=value([facts[0][short],min(facts[1].values())])
for item in ['B','D']: assert (lo,hi)==(D(key[item]['lo']),D(key[item]['hi']))
assert value([rows[long] for rows in facts])==D(key['C']['lo'])==D(key['C']['hi'])
with (base/'scoring/annotations.csv').open() as f: annotations=list(csv.DictReader(f))
assert len(annotations)==len({r['run'] for r in annotations})==8
assert [r['run'].replace('_txt','_text') for r in annotations]==protocol['schedule']
results=[]
for a in annotations:
    run=a['run']
    item,ext=run.split('_')
    sent=read(base/'raw'/f'{run}.sent.json')
    raw=read(base/'raw'/f'{run}.answer.json')
    assert len(sent['attachments'])==3 and sent['verifiedAttachmentControls']
    k=key[item]
    l,u,cap=map(D,[k['lo'],k['hi'],k['limit']])
    form='point' if l==u else 'interval'
    expected='within' if u<=cap else 'over' if l>cap else 'undetermined'
    assert expected==k['decision']
    assert all(re.search(r'(?<![\d.])'+re.escape(v)+r'(?!\d)',raw['text']) for v in [a['reported_low_or_point'],a['reported_high']] if v)
    err=max(abs(D(a['reported_low_or_point'])-l),abs(D(a['reported_high'] or a['reported_low_or_point'])-u))
    results.append({**a,'reference_low':l,'reference_high':u,'max_abs_error_pp':err,'form_correct':int(a['form']==form),'numeric_correct':int(err<=D('.005') and a['form']==form),'decision_correct':int(expected==a['decision']),'answer_text_sha256':hashlib.sha256(raw['text'].encode()).hexdigest()})
with (base/'scoring/case_scores.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=results[0]);w.writeheader();w.writerows(results)
for ext in ('pdf','txt'):
    subset=[r for r in results if r['run'].endswith('_'+ext)]
    print(ext,{k:sum(int(r[k]) for r in subset) for k in ['form_correct','numeric_correct','decision_correct','dated_sources_and_pages']},'of',len(subset))
