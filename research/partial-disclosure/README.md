# Partial holdings: a missing row is not a zero

**中文：只披露前十大持仓时的穿透区间。** 目标资产没出现在表里，不代表持仓为零。研究要区分“确定值”“可识别范围”和“信息不足”，并检验模型是否主动说明这一点。

## Question and bound

Assume a complete top-ten ranking of nonnegative holdings in a comparable reporting unit. If a target is absent, its fraction is between zero and the smaller of the tenth holding and the residual undisclosed mass. For account weights qⱼ, the endpoint bounds combine linearly across parent funds.

Illustrative constructed account: 60% in one parent where the target is absent and the tenth holding is 3.2%, plus 40% in a parent reporting 5.0%. With enough residual mass, account exposure lies in **[2.00%, 3.92%]**. This example is explanatory, not a newly observed fund account. Short positions, incomplete rankings, inconsistent share classes or different reporting bases require a different bound.

## Completed clean-table pilot

The frozen set has **20 prompts: 10 point controls and 10 interval questions**, balanced between an explicit reminder and a heading-only disclosure cue. Inputs use source-derived BlackRock/Vanguard tables and constructed account weights.

- The local reasoning-enabled Qwen3-8B configuration asserted a point on all ten interval questions.
- GPT-6 High answered all 20 correctly under the recorded scoring rules.
- Gemini returned 14 original answers, all correct; four separately labeled technical recoveries were also correct. Two answers remained absent. Recovery answers are not counted as first answers.

The primary hosted numeric tolerance was **0.005 percentage points**, with 0.001 reported alongside it. This differs from the 0.5-percentage-point exposure tolerance used in earlier portfolio experiments. The dated amendment followed local P07 but preceded hosted collection. Answer type remains central.

## Retained value and stopping decision

The useful deliverables are the interval answer key, explicit assumptions, blind prompts and failure/missingness handling. The observed hosted answers did not support a broad strong-model failure claim. The original two-model formal stopping condition remained unresolved because of missing Gemini first responses.

## Materials

- [All 20 prompts](prompts.jsonl), [gold intervals](gold.csv), [prompt hashes](manifest.json), [source tables](fund_tables.json), [original independent bound checker](original_verify.py).
- [Local raw answers](local_qwen3_raw.jsonl), [local scores](local_scores.json), [GPT item scores](gpt_case_scores.csv), [Gemini item scores](gemini_case_scores.csv), [collection status](collection_status.json).
- [Hosted result report](../../archive/reports/Top10_Gemini_and_GPT6_Results.pdf), [dated scoring amendment](../../archive/reports/Top10_Hosted_Scoring_Amendment_2026-11-06.txt), [complete prompt package](../../archive/packages/Top10_Disclosure_Pilot_20.zip), [hosted evidence](../../archive/packages/Top10_Hosted_Reasoning_Results.zip).

## Files, provenance and reproduction

The files beside this README are byte-for-byte browsing copies of the previously published archives. Some original scripts depend on their original directory layout: use the complete package for execution, or run the repository-level historical reproduction command below. Filenames were shortened for navigation; their original paths and hashes are in [the source map](../source-map.json). The complete archives preserve additional prompts, raw outputs, protocols, manuscripts and supporting files.

```bash
python3 tools/reproduce_historical.py
```

Run that command from the repository root with NumPy and SciPy installed. It checks archived evidence and reference arithmetic, without making model requests. This navigation and commentary were added retrospectively on 9 November 2026; they are not new experiments or a new preregistration. These topics overlap and must not be counted as independent studies or accepted publications.
