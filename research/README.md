# Financial text and portfolio research collection

[中文总览](README.zh-CN.md) · [Full research journey](../docs/research-journey.md) · [Current disclosure-timing paper](../paper/main.pdf)

This collection makes the earlier work visible alongside the final disclosure-code paper. It preserves questions, algorithms under explicit assumptions, constructed test cases, source-derived holdings, raw model responses, corrections and negative results. The seven entries are **overlapping research strands**, not seven independent publications or disjoint sample sets.

| Strand | Core question | What can be inspected |
| --- | --- | --- |
| [Textual fragmentation](text-fragmentation/README.md) | Can equivalent descriptions change exposure or risk answers? | Original case/prompt bank, generator, pilot and cue-confounding analyses |
| [Portfolio risk](portfolio-risk/README.md) | Did the model read holdings correctly, calculate exposure correctly and calculate risk correctly? | Joint-output evidence and the limits of a correct risk number |
| [Look-through exposure](exposure-lookthrough/README.md) | Are funded amounts and underlying holdings assigned and aggregated correctly? | 536 recorded responses, controlled/source prompts, ledgers, parser and source-failure census |
| [Aggregation diagnostics](aggregation-diagnostics/README.md) | When can incorrect weighting pass a correct-answer test? | Full derivations, contrast identification, 86 exact-checkable certificate records and zero-coverage result |
| [Reasoning-configuration recheck](reasoning-recheck/README.md) | Do the earlier total errors survive a stronger configuration? | All 100 paired prompts/answers and the correction from 35/100 to 98/100 |
| [Incomplete disclosure](partial-disclosure/README.md) | Does an absent top-ten holding call for a point or an interval? | 20 blind prompts, checked bounds and complete item-score records |
| [Original-document reading](document-reading/README.md) | Does realistic PDF input change the result? | Four PDF/text pairs, all saved answers and source references |

## A useful reading route

Start with **look-through exposure** for the accounting and observed field errors. Read the **reasoning recheck** immediately after it. Then read **aggregation diagnostics** for the mathematical work and **textual fragmentation** for the original hypothesis. Partial disclosures and original documents show how the research question developed toward historical availability.

## What is original and what was added for this collection

- All copied data, raw answers, historical LaTeX and original scripts are byte-identical to their published source archive members. [Source map](source-map.json).
- These explanatory READMEs and the browsing layout were written retrospectively on 9 November 2026. They do not backdate a protocol or create new results.
- [Historical reproduction script](../tools/reproduce_historical.py) validates selected old evidence in temporary copies. [Verification result](historical-verification.json).
- Scripts named `original_*` are reference copies; execute the complete archive layout or the repository-level reproduction command. No LLM inference is triggered by that command.
- [Version and artifact index](../docs/artifact-index.md) retains the full v5, v8 and v9 manuscripts and complete packages. No original manuscript was replaced by these summaries.

The strongest retained lesson is methodological: a correct total is not always an informative test; reported fields, arithmetic, representation changes and unavailable information need different controls. Claims weakened by subsequent experiments remain visible beside the original result.
