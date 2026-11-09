# Research journey: how the question changed

**Retrospective synthesis prepared 9 November 2026.** This narrative was written after the results. It is not a preregistration. Contemporaneous freezes, amendments, raw responses, and historical manuscripts remain in the indexed evidence packages.

The project did not begin with a 60-day N-PORT floor. It began with a broader interest in financial text: can a model distinguish changes in how a portfolio is described from changes in what the portfolio actually holds? The useful result emerged by repeatedly testing whether an apparent failure still existed under a more appropriate baseline.

## 1. Textual fragmentation was a hypothesis, not a finding

One investment can be described as one product or several funded lots. Under controlled assumptions excluding wrapper-specific risks and costs, equivalent holdings imply equivalent exposure and risk. The initial question was whether additional product names would produce a false impression of diversification.

The early small-model pilot recorded 472 responses. It did not establish that behavioral explanation. An illustrative risk value contaminated outputs: changing the example changed the returned number. Exposure extraction and risk arithmetic also failed differently. A reported difference in risk could therefore not be attributed specifically to a diversification bias.

**Decision:** retain the raw pilot and reject the strong interpretation. The useful question became what a test can identify, rather than whether one answer looks plausible. See the historical [v5 manuscript](../archive/reports/Portfolio_Risk_Text_Fragmentation_English_v5.pdf), especially its pilot appendix.

## 2. A correct answer can be an uninformative test

Suppose account weights are 25% and 75%. If both products hold 60% of Asset A, correct weighting, equal product weighting, and dropping one product all give 60% after normalization. Now change the products to 30% and 70% A: the correct account exposure is still 60%, but those incorrect rules separate.

This led to the homogeneous-holdings blind spot and a contrast-basis diagnostic for a **fixed normalized linear weighting rule**. The derivation is useful under its assumptions. It does not identify arbitrary language-model computation.

The diagnostic itself was evaluated. It accepted no cases in the tested initial setting. A post-hoc convex-compatibility analysis excluded the proposed fixed-rule explanation for the saved response traces at the stated tolerance. That is evidence about the inadequacy of the explanatory class, not a working universal verifier. The [32-page v8 integration](../archive/reports/Portfolio_Risk_Integrated_v8.pdf) preserves this development and its limits.

**What survives:** design examples that force plausible incorrect implementations to disagree. **What does not survive:** claiming that a theorem about a restricted error class certifies a general model.

## 3. Separate the interface, reported facts, and computation

The next portfolio experiments distinguished requested JSON structure, extracted source fields, model-reported totals, and calculator totals. Correct fields could coexist with incorrect arithmetic. Conversely, an accurate calculator could not repair the wrong source assignment. A schema violation could hide otherwise usable numbers.

This decomposition remained useful even when the original practical failure story weakened. It prevents a formatting problem from being presented as a financial reasoning failure, and prevents a correct aggregate from certifying source extraction.

## 4. A reasoning-configuration recheck changed the practical claim

A separate 100-response recheck used the same checkpoint and input texts with a revised reasoning/runtime configuration. The report records:

| Subset | Original correct totals | Recheck correct totals |
| --- | --- | --- |
| Homogeneous controlled | 24/24 | 24/24 |
| Heterogeneous controlled | 4/24 | 24/24 |
| Published-table direct | 2/26 | 25/26 |
| Published-table ledger | 5/26 | 25/26 |

Cases with a correct ledger but wrong reported total fell from 18/26 to 0/26. Two responses were truncated. Thinking, sampling, output budget, context, and batching changed together, so the improvement cannot be attributed to thinking alone. Previously examined cases were reused; this was not a new blind holdout.

**Decision:** narrow the practical claim. The mathematical blind spot remains true, but by itself it does not establish a hard deployment problem for the improved configuration. The [complete recheck note](../archive/reports/Portfolio_Risk_Thinking_Recheck_Report.txt) and companion archive preserve the unfavorable evidence alongside the earlier manuscripts.

## 5. Incomplete disclosure: a useful distinction, but no strong-model signal in the clean task

Top-ten fund disclosures motivated a different question. If a target is absent, zero is not generally identified: under the stipulated ranking/nonnegative-holdings assumptions, its weight is bounded. The correct answer can be an interval.

The local reasoning-enabled Qwen3-8B configuration asserted a point on all ten interval questions. GPT-6 High answered all ten point controls and all ten interval questions correctly. Gemini's 14 original returned answers were also correct; four technical recoveries increased the observed total to 18, leaving two absent. Recoveries were not silently promoted to first responses.

The hosted scoring amendment was frozen before the hosted questions were sent, but after seeing local P07. It used 0.005 percentage points as primary numeric tolerance, retained 0.001 in parallel, and scored the explicitly supplied higher-precision value when both precise and rounded versions appeared. Answer type remained central.

**Decision:** no positive observed signal for a broad hosted-model failure claim. The original two-model stopping criterion remained unresolved because of missing Gemini first responses. See the [combined report](../archive/reports/Top10_Gemini_and_GPT6_Results.pdf) and [dated scoring amendment](../archive/reports/Top10_Hosted_Scoring_Amendment_2026-11-06.txt).

## 6. More pages did not automatically create a harder problem

An original-document pilot supplied a 510-page BlackRock annual report and later factsheets, compared with matched extracted text. GPT-6 High returned correct exposure, limit decision, and source pages in all four PDF and all four text questions. It rejected carrying a precise older holding into the newer incomplete disclosure.

This was a bundled product workflow with unobserved internal retrieval, one account, one issuer, and three distinct exposures. It did not prove general PDF competence or test historical public availability. It did show that adding a large PDF was insufficient, in these cases, to establish the proposed failure. [Report](../archive/reports/BlackRock_Original_PDF_Pilot.pdf).

## 7. Move from the holdings date to the knowledge date

A temporal-disclosure pilot then asked which reports were available at a simulated decision time. Forty first requests were attempted per product: GPT returned 40, Gemini 36. GPT made three wrong limit decisions in the original series; Gemini made two on its observed series. Different source mistakes could lead to the same false alert, and some source mistakes left the limit decision unchanged. Subsequent GPT gray-zone follow-ups were all correct and remained a separate sample.

The [two-page report](../archive/reports/PIT_Disclosure_Pilot_Results.pdf) separates decision, numeric, schema, and source-chain scores. A [holiday-weekend 13F pair](../archive/reports/Holiday_13F_Check.pdf) was also correct, while its wording could not distinguish transmission-start from acceptance-time reasoning because both timestamps fell after the cutoff.

**Lesson:** specify the unit of failure. A wrong source, unsupported precise exposure, wrong limit decision, and malformed output are not interchangeable outcomes.

## 8. A partial rule panel isolated an N-PORT lead

The next locally frozen panel contained 44 prompts per vendor. GPT returned all 44. Gemini returned 17 of 21 attempted requests, leaving four technical missing and 23 unattempted. This was not 88 completed answers.

GPT's original 16 unaided applications were correct, but the additional N-PORT release application was wrong. Giving the rule text corrected it; an explicit deadline/release diagnostic was correct. Both of GPT's direct-rule errors also concerned N-PORT. These formulation-dependent responses do not prove a latent state of “knowing but refusing to use” the correct rule.

**Decision:** the registered broad cross-family expansion criterion was not met. Preserve that result. Follow the narrower clue into implementation, without rewriting the stopping rule. The public metadata audit separately established how much delay a hypothetical 60-day floor would create.

## 9. Test executable behavior, not only verbal answers

The code pilot crossed three schemas and three prompts. It produced 50 primary answers plus four separately recorded technical recoveries. Frozen future-information interventions targeted the first two report periods. No dated numerical leakage witness was found.

A post-hoc full-horizon audit checked all six periods and 477 decision dates. It exposed the central descriptive pattern: 10/12 GPT dated P0/P1 programs matched a maximum-based 60-day floor. A further program used strict filing dates. One whole-output refusal concerned the missing next execution session and was corrected from “valid abstention” to an interface failure.

**Decision:** report the absence of observed look-ahead honestly, while investigating excessive withholding as a different error. Passing a one-sided leakage test does not establish functional correctness.

## 10. Use a counterexample to constrain the explanation

A separately frozen 36-answer follow-up paired N-PORT and Form 13F descriptions, three prompts, three repetitions, and two vendors. GPT and Claude reproduced N-PORT floors. Neither imposed the analogous 45-day floor on 13F. The fixture sensitivity audit established that such a floor would have been observable.

An explicit filing-date contract produced reference-aligned code in all 12 follow-up P2 answers. Calendar-adjusted variants discovered after collection started stayed exploratory rather than being added retrospectively to the frozen classifier.

**Conclusion supported:** an inapplicable N-PORT publication rule was executed in these samples. **Stronger explanation not supported:** a universal habit of treating every filing deadline as a release date, or proof that the model internally recalled a particular historical document.

## What connects the stages

There is a recurring evaluation lesson, not a claim that all stages measure one effect: a system can pass a weak check for the wrong reason. Homogeneous portfolios do not separate weighting rules. Correct totals do not establish correct extraction. No future-information witness does not establish correct availability. The next experiment should therefore distinguish competing explanations before adding more examples.

The final paper is a bounded empirical contribution. The archive also preserves reusable methodological work: error decomposition, discriminating controls, failure-aware scoring, prospective versus retrospective labels, and decisions to stop unproductive expansion.
