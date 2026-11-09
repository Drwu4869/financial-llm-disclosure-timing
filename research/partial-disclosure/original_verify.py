"""Validate the answer key from exactly the tables visible in each blinded prompt."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import csv,hashlib,json,math,re
from scipy.optimize import linprog
root=Path(__file__).resolve().parent
keys={r['id']:r for r in csv.DictReader((root/'answer_key/gold.csv').open())};prompts=[json.loads(s) for s in (root/'prompts.jsonl').read_text().splitlines()];manifest=json.loads((root/'manifest.json').read_text());tables={f['id']:f for f in json.loads((root/'sources/original_tables.json').read_text())};assert len(keys)==len(prompts)==len({v['id'] for v in prompts})==20
for p in prompts:
 i=p['id'];q=p['prompt'];key=keys[i];assert (root/'blind_prompts'/(i+'.txt')).read_text()==q+'\n';assert hashlib.sha256(q.encode()).hexdigest()==manifest['prompt_sha256'][i];parts=q.split('\n\n');assert len(parts)==4
 g=re.search(r'allocates (\d+)% to the first parent and (\d+)% to the second\. Target security: (.+?)\.',parts[-1]);assert g
 # Names may contain periods, e.g. U.K. Get the target up to the fixed question/reminder instead.
 label=parts[-1].split('Target security: ',1)[1].split('. The disclosed lists',1)[0].split('. What percentage',1)[0]
 assert label==key['target'];weights=[Q(g[k],) / 100 for k in (1,2)];assert sum(weights)==1
 lo=hi=Q(0);lp_lo=lp_hi=0.0
 for j,block in enumerate(parts[1:3]):
  rows=[(name,Q(value.removesuffix('%'))) for name,value in (ln.rsplit(' | ',1) for ln in block.splitlines()[1:])];vs=[x[1] for x in rows];assert len(rows)==len(dict(rows))==10 and vs==sorted(vs,reverse=True)
  dic=dict(rows);remaining=100-sum(vs);cap=vs[-1];assert remaining>0 and cap>0;w=weights[j]
  if label in dic: a=b=dic[label];x=y=float(a)
  else:
   a,b=Q(0),min(cap,remaining);n=1+math.ceil(remaining/cap);c=[1.0]+[0.0]*(n-1);kwargs={'A_eq':[[1.]*n],'b_eq':[float(remaining)],'bounds':[(0,float(cap))]*n,'method':'highs'};l=linprog(c,**kwargs);h=linprog([-v for v in c],**kwargs);assert l.success and h.success;x,y=l.fun,-h.fun
  lo+=w*a;hi+=w*b;lp_lo+=float(w)*x;lp_hi+=float(w)*y
 assert (lo,hi)==(Q(key['lower_pct']),Q(key['upper_pct'])) and abs(float(lo)-lp_lo)<1e-8 and abs(float(hi)-lp_hi)<1e-8;assert (lo==hi)==(key['answer_kind']=='point')
 if key['publisher']=='Vanguard':
  actual=sum(w*Q(next(v['percent'] for v in tables[key['parent_'+ab]]['rows'] if v['holding']==label)) for ab,w in zip('AB',weights));assert actual==Q(key['hidden_full_table_check_pct']) and lo<=actual<=hi
  if lo<hi:assert lo<actual
assert Counter((v['answer_kind'],v['reminder']) for v in keys.values())=={(t,h):5 for t in ['point','interval'] for h in ['repeated','heading only']};print('PASS: 20 blind prompts, 10 point answers, 10 independently bounded intervals and 5 positive withheld targets.')
for s in json.loads((root/'sources/source_manifest.json').read_text()):
 p=root/'sources/pdf'/(s['name']+'.pdf');
 if p.exists():assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256']
