"""Scores only observable reports; never infers a hidden reasoning process."""
from fractions import Fraction as F
import json

def number(x):
    if type(x) not in (int,float):raise ValueError('JSON number required')
    return F(str(x))

def score(prompt,record):
    g=F(prompt['gold_percent_exact']);s={'direct_valid':False,'answer_correct':False,'absolute_error':None,'ledger_valid':False,'ledger_exact':False,'calculator_correct':False,'calculator_error':None,'answer_matches_own_ledger':False,'correct_total_wrong_ledger':False,'correct_total_wrong_valid_ledger':False,'finish_reason':record.get('response',{}).get('choices',[{}])[0].get('finish_reason')}
    try:
        obj=json.loads(record['raw_text'])
    except (KeyError,TypeError,ValueError):return s
    try:
        y=number(obj['total_a_percent']);assert 0<=y<=100
        s.update(direct_valid=True,answer_correct=abs(y-g)<=F(1,2),absolute_error=float(abs(y-g)))
    except (KeyError,TypeError,ValueError,AssertionError,ZeroDivisionError):pass
    if prompt['method']=='ledger':
        try:
            rows=obj['rows'];assert isinstance(rows,list) and len(rows)==len(prompt['gold_rows'])
            mapped={}
            for row in rows:
                assert isinstance(row,list) and len(row)==3
                lot=number(row[0]);assert lot.denominator==1 and int(lot) not in mapped
                amount=number(row[1]);a=number(row[2]);assert amount>=0 and 0<=a<=100
                mapped[int(lot)]=(amount,a)
            assert set(mapped)=={r['lot'] for r in prompt['gold_rows']}
            total=sum(x[0] for x in mapped.values());assert total>0
            cal=sum(amount*a for amount,a in mapped.values())/total
            exact=all(abs(mapped[r['lot']][0]-r['amount_gbp'])<=F(1,200) and abs(mapped[r['lot']][1]-r['a_percent'])<=F(1,20000) for r in prompt['gold_rows'])
            s.update(ledger_valid=True,ledger_exact=exact,calculator_correct=abs(cal-g)<=F(1,2),calculator_error=float(abs(cal-g)),answer_matches_own_ledger=s['direct_valid'] and abs(y-cal)<=F(1,2))
        except (KeyError,TypeError,ValueError,AssertionError,ZeroDivisionError):pass
        s['correct_total_wrong_ledger']=s['answer_correct'] and not s['ledger_exact']
        s['correct_total_wrong_valid_ledger']=s['answer_correct'] and s['ledger_valid'] and not s['ledger_exact']
    return s
