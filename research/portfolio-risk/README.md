# Portfolio risk: separate reading from calculation

**中文：投资组合风险研究。** “读对持仓”“算对穿透暴露”“根据暴露算对风险”是三个不同步骤。这里保留风险公式、联合输出实验和错误分解；不把标准投资组合公式包装成新算法。

## Research question and accounting

Let q be account allocations to products and B their underlying-asset compositions. Standard accounting gives w = Bᵀq. Given a fixed return covariance matrix, classical portfolio standard deviation is

$$\sigma(w)=\sqrt{w^\top\Sigma w}.$$

These are established formulas. A correct final standard deviation does not generally identify the weights that produced it. With equal asset variances and zero covariance, a 20/80 portfolio and an 80/20 portfolio have the same variance, although their exposures differ.

The experiments requested both exposure and risk, so that a reported risk could be compared with (i) risk from the true holdings and (ii) risk recomputed from the model's own reported holdings.

## Recorded result and its scope

In the early Qwen2.5-3B joint-output diagnostic, **15/16 responses reported correct exposures**, but **none of those 15 risk values fell within the stated 5% relative tolerance**. The saved analysis also records inconsistency with the model's own reported weights in all 16 responses.

This is a small, historical and prompt-confounded diagnostic. It separates observable errors; it does not establish a persistent problem in current reasoning models or reveal their hidden reasoning. The later 100-response recheck measured **exposure totals**, not a full replication of this risk-standard-deviation task. Its improvements must not be silently relabeled as risk results.

## Why retain it

The useful engineering idea is to audit intermediate reported facts and recompute authorized arithmetic independently. An arithmetic tool can repair a wrong calculation from correct inputs; it cannot repair a wrongly extracted holding. The source-assignment examples in [look-through exposure](../exposure-lookthrough/README.md) show that second failure mode.

## Evidence

- [Joint-output analysis, including all 16 records](joint_qwen3_analysis.json) and [joint prompt bank](joint_prompts.jsonl).
- [Original analysis code](original_analyze_joint.py), with its original dependencies retained in the [v5 package](../../archive/packages/Portfolio_Risk_LaTeX_and_Evidence_v5.zip).
- [Full accounting and diagnostic derivation](../aggregation-diagnostics/theory.tex), [v5 paper](../../archive/reports/Portfolio_Risk_Text_Fragmentation_English_v5.pdf).

## Files, provenance and reproduction

The files beside this README are byte-for-byte browsing copies of the previously published archives. Some original scripts depend on their original directory layout: use the complete package for execution, or run the repository-level historical reproduction command below. Filenames were shortened for navigation; their original paths and hashes are in [the source map](../source-map.json). The complete archives preserve additional prompts, raw outputs, protocols, manuscripts and supporting files.

```bash
python3 tools/reproduce_historical.py
```

Run that command from the repository root with NumPy and SciPy installed. It checks archived evidence and reference arithmetic, without making model requests. This navigation and commentary were added retrospectively on 9 November 2026; they are not new experiments or a new preregistration. These topics overlap and must not be counted as independent studies or accepted publications.
