"""Audit the saved requests and answers against the registered 100 matched inputs."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def read_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]

def indexed(rows):
    result = {row['request_id']: row for row in rows}
    assert len(result) == len(rows), 'Duplicate question ID'
    return result

def audit():
    cfg = json.loads((ROOT/'data/protocol.json').read_text())
    for name, digest in cfg['files'].items():
        assert sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    raw = ROOT/'results/evaluation/raw.jsonl'
    before = indexed(read_rows(ROOT/'data/baseline_raw.jsonl'))
    after = indexed(read_rows(raw))
    prompts = indexed(read_rows(ROOT/'data/prompts.jsonl'))
    assert len(prompts) == 100 and before.keys() == prompts.keys() == after.keys()
    model = json.loads((ROOT/'runtime/model_manifest.json').read_text())
    for key, prompt in prompts.items():
        old, new = before[key]['request_payload'], after[key]['request_payload']
        messages = [{'role':'system','content':prompt['system']}, {'role':'user','content':prompt['prompt']}]
        assert new['messages'] == old['messages'] == messages, key
        assert new['model'] == old['model'] == model['model_id'], key
        assert new['response_format'] == old['response_format'] == {'type':'json_object'}, key
        assert new['chat_template_kwargs']['enable_thinking'] is True, key
        for param in ('temperature','top_p','top_k','min_p','seed','max_tokens'):
            assert new[param] == cfg[param], (key,param)
        assert sha256(json.dumps(new,sort_keys=True).encode()).hexdigest() == after[key]['request_sha256'], key
        if after[key]['status'] == 'response_received':
            msg = after[key]['response']['choices'][0]['message']
            assert after[key]['raw_text'] == msg.get('content'), key
        lots = prompt['gold_rows']
        weights = [Fraction(str(x['amount_gbp'])) for x in lots]
        reconstructed = sum(w*Fraction(x['a_percent']) for w,x in zip(weights,lots))/sum(weights)
        assert reconstructed == Fraction(prompt['gold_percent_exact']), key
    recovery = json.loads((ROOT/'runtime/restoration_after_69.json').read_text())
    n = recovery['restored_checkpoint_records']
    prefix = b''.join(raw.read_bytes().splitlines(keepends=True)[:n])
    assert sha256(prefix).hexdigest() == recovery['restored_raw_prefix_sha256']
    result = {'unique_matched_ids':len(after),'request_text_and_json_constraints_matched':100,'new_request_payload_hashes_matched':100,'gold_totals_recomputed':100,'restored_prefix_preserved':n,'evaluation_raw_sha256':sha256(raw.read_bytes()).hexdigest()}
    return result

if __name__ == '__main__':
    print(json.dumps(audit(),indent=2))
