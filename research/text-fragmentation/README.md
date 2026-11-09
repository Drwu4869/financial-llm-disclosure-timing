# Textual fragmentation and financial invariance

**中文：文本碎片化研究。** 同一份持仓，写成一个产品、八个产品或多笔投入，经济暴露相同时，模型的判断是否应保持一致？这里保留原始问题、提示词、案例和后来推翻强解释的证据。

## Research question

Does changing the description of an economically equivalent portfolio change its extracted exposure or reported risk? The controlled task excludes wrapper-specific fees, taxes, leverage and additional risks. Real wrappers are not assumed to be interchangeable.

For example, one £10,000 holding with 60% A and 40% B can be described as eight separately funded £1,250 lots of the same composition. Its account-level A exposure remains £6,000. A genuine change in holdings is a different control, not an invariant rewrite.

## What was built and learned

- A constructed text generator covering merged/fragmented descriptions, verified-weight inputs, canonical inputs, extraction-plus-calculator conditions and genuine exposure changes.
- The released v3 input bank contains **32 cases and 480 prompt records**, split into 16 development and 16 evaluation cases, with 240 prompt records in each split. This is a prompt-bank count, not 480 completed generations. It supersedes the initial brainstorming description of 30/30/180; those proposal numbers are not used as observed sample sizes.
- The historical pilot and extensions recorded **472 small-model responses** in total. They are not a clean estimate of fragmentation bias. The 1.5B cue-sensitivity analysis records eight risk responses that followed the changed illustrative number after numerical normalization, with none within the specified 5% risk tolerance.
- Weight normalization could appear successful when different mistakes happened to produce the same aggregate. That prompted matched heterogeneous controls and the [aggregation diagnostic](../aggregation-diagnostics/README.md).

## What remains valuable

The reusable contribution is the **experimental design and identification problem**: distinguish an economically irrelevant rewrite, a genuine portfolio change, a prompt-number artifact and a calculation error. The strong claim that these experiments discovered a general LLM diversification bias was not established.

## Read the original work

- [22-page v5 paper](../../archive/reports/Portfolio_Risk_Text_Fragmentation_English_v5.pdf) and [complete source/evidence package](../../archive/packages/Portfolio_Risk_LaTeX_and_Evidence_v5.zip).
- [Original constructed cases](cases.jsonl), [all frozen prompt records](prompts.jsonl), [answer key](answer_key.jsonl), [protocol](protocol.json), [generator source](original_build_experiment.py).
- [1.5B analysis](pilot_qwen15_analysis.json), [3B analysis](pilot_qwen3_analysis.json), [post-hoc cue check](cue_sensitivity.json).
- [Later reasoning recheck](../reasoning-recheck/README.md): important qualification, not a rerun of every fragmentation condition.

## Files, provenance and reproduction

The files beside this README are byte-for-byte browsing copies of the previously published archives. Some original scripts depend on their original directory layout: use the complete package for execution, or run the repository-level historical reproduction command below. Filenames were shortened for navigation; their original paths and hashes are in [the source map](../source-map.json). The complete archives preserve additional prompts, raw outputs, protocols, manuscripts and supporting files.

```bash
python3 tools/reproduce_historical.py
```

Run that command from the repository root with NumPy and SciPy installed. It checks archived evidence and reference arithmetic, without making model requests. This navigation and commentary were added retrospectively on 9 November 2026; they are not new experiments or a new preregistration. These topics overlap and must not be counted as independent studies or accepted publications.
