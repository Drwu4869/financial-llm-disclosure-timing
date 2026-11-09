# When correct totals cannot identify correct aggregation

**中文：同质持仓的测试盲区与诊断公式。** 这一部分保留之前较多的数学推导：为什么答对也可能没算对、怎样设计有区分力的扰动、怎样证明一组回答不能由固定权重解释。公式的条件和实验失败也一并保留。

## The blind spot

For a fixed normalized linear rule f(b) = pᵀb with nonnegative weights summing to one, homogeneous compositions b = a₀1 give f(b) = a₀ whatever p is. Dropping, duplicating or incorrectly weighting a product can therefore remain invisible.

For account weights (25%, 75%), both products at 60% A give 60% under correct weighting, equal weighting and dropping either product. Change their compositions to (30%, 70%): the correct total stays 60%, whereas equal weighting gives 50%, dropping the first gives 70%, and duplicating the first before renormalization gives 54%.

## Conditional method retained from v5–v9

Centered composition perturbations produce g = Cp **if the same linear rule p is used across queries**. Together with normalization, they identify p when

$$\operatorname{rank}\begin{bmatrix}\mathbf 1^\top\\C\end{bmatrix}=J.$$

The four-product design uses three Hadamard contrasts, giving an explicit reconstruction and a noise bound. A second, post-hoc diagnostic asks how closely any fixed convex combination can explain a saved answer vector:

$$d_*(X,y)=\min_{p\ge0,\;\mathbf1^\top p=1}\|y-Xp\|_\infty.$$

Primal/dual witnesses provide independently checkable rational bounds. Linear algebra, finite differences, convex optimization and duality are established methods; this archive's contribution is their scoped application and evaluation, not a claim to invent those methods.

## What the tests actually showed

| Evidence | Recorded outcome | Meaning |
| --- | --- | --- |
| Deterministic fault injection | 3,840 specified linear rules; all pass the homogeneous base; all 3,744 nonuniform distortions detected by three contrasts | Validates the restricted mathematics, not LLM performance |
| LLM acceptance gate | Zero accepted cases in the evaluated configurations | No useful correctness-verifier coverage was demonstrated |
| Exact-checkable certificates | 86 records: 22 strict Qwen + 64 normalized records across two models | Overlapping views, not 86 independent observations |
| Normalized fixed-rule compatibility | 32/32 vectors per model incompatible at fractional error budget 0.005 (0.5 percentage points) | Rejects a fixed-rule explanation of those traces |

One Qwen trace required a minimum error of 3⅓ percentage points even though the specified single-query, pair and midpoint witness families missed it. This is a finite-trace diagnosis, not proof of a new generally superior verifier.

## Preserved mathematics and code

- [Full theory](theory.tex), [certificate method and proof](certificate_method.tex), [certificate results and worked contradiction](certificate_results.tex).
- [86 complete certificates](certificates.jsonl), [exact rational checker source](original_verify_certificates.py), [summary](certificate_summary.json), [fault-injection summary](fault_injection_summary.json).
- [Frozen follow-up protocol](protocol.json), [constructed cases](cases.jsonl), [v8's 32-page integration](../../archive/reports/Portfolio_Risk_Integrated_v8.pdf), [v9 full manuscript](../../archive/reports/Portfolio_Exposure_v9_Full.pdf).

## Files, provenance and reproduction

The files beside this README are byte-for-byte browsing copies of the previously published archives. Some original scripts depend on their original directory layout: use the complete package for execution, or run the repository-level historical reproduction command below. Filenames were shortened for navigation; their original paths and hashes are in [the source map](../source-map.json). The complete archives preserve additional prompts, raw outputs, protocols, manuscripts and supporting files.

```bash
python3 tools/reproduce_historical.py
```

Run that command from the repository root with NumPy and SciPy installed. It checks archived evidence and reference arithmetic, without making model requests. This navigation and commentary were added retrospectively on 9 November 2026; they are not new experiments or a new preregistration. These topics overlap and must not be counted as independent studies or accepted publications.
