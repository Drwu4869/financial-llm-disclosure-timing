# A 100-response recheck that changed the conclusion

**中文：推理配置复验。** 这个方向也值得展示：新实验大幅削弱了早期“模型不会算暴露”的结论，因此保留完整前后对照，并据此调整研究判断。

## Paired observation

The recheck reused 100 previously examined input texts with the same checkpoint and quantization, but changed thinking, sampling, seed, output allowance, context and batching together. It tests a **configuration change**, not the isolated causal effect of thinking.

| Subset | Original | Recheck |
| --- | --- | --- |
| Homogeneous controlled totals | 24/24 | 24/24 |
| Heterogeneous controlled totals | 4/24 | 24/24 |
| Published-table direct totals | 2/26 | 25/26 |
| Published-table ledger-prompt totals | 5/26 | 25/26 |
| Correct source ledger but wrong model total | 18/26 | 0/26 |

The four total-score rows sum to **35/100 → 98/100**. The last row overlaps the source-ledger subset and is not added to that total. Two unsuccessful recheck outputs were length-terminated at a 4,096-token cap and stayed in the denominator. Four engineering development responses are excluded.

## What changed

The old practical failure claim had to be narrowed. The homogeneous-test blind spot remains mathematically true, but it alone does not establish a hard deployment problem under the improved configuration. These were previously examined cases, not a new blind holdout, and only merged controlled direct prompts were rechecked; all fragmentation and changed-exposure conditions were not rerun.

The research value is an auditable decision to revise a claim, plus a clean separation of schema validity, extracted facts, computed totals and truncation. It is not evidence that every reasoning model solves every financial task.

## Complete paired evidence

- [100 exact prompts and gold rows](prompts.jsonl), [100 original responses](baseline_raw.jsonl), [100 recheck responses](recheck_raw.jsonl).
- [Frozen protocol](protocol.json), [counts](counts.csv), [full analysis](analysis.json), [original analysis](original_analyze.py), [scorer](original_score.py), [request/provenance checker](original_verify_provenance.py).
- [Full contemporaneous result note](../../archive/reports/Portfolio_Risk_Thinking_Recheck_Report.txt), [report PDF](../../archive/reports/Portfolio_Risk_Recheck_Results.pdf), [complete reproducible package](../../archive/packages/Portfolio_Risk_Thinking_Recheck.zip).

## Files, provenance and reproduction

The files beside this README are byte-for-byte browsing copies of the previously published archives. Some original scripts depend on their original directory layout: use the complete package for execution, or run the repository-level historical reproduction command below. Filenames were shortened for navigation; their original paths and hashes are in [the source map](../source-map.json). The complete archives preserve additional prompts, raw outputs, protocols, manuscripts and supporting files.

```bash
python3 tools/reproduce_historical.py
```

Run that command from the repository root with NumPy and SciPy installed. It checks archived evidence and reference arithmetic, without making model requests. This navigation and commentary were added retrospectively on 9 November 2026; they are not new experiments or a new preregistration. These topics overlap and must not be counted as independent studies or accepted publications.
