NO LOOK-AHEAD, YET TOO LATE
Inapplicable Disclosure Rules in LLM-Generated Backtest Code
Changyi Wu | Layout and factual precision revision | 9 November 2026

READING AND EDITING
main.tex is the manuscript entry point. The compiled paper has 9 pages,
including references and appendices, 4 figures, 5 tables and a practitioner checklist.
All principal experimental
findings and qualifications appear in the paper, not only in this archive.
references.bib contains 20 primary-source references. main.bbl is
included as a compilation fallback. figures/ contains vector PDF figures.

Build with a normal TeX Live or MiKTeX installation:
  bash build.sh
Or upload this directory as a ZIP to Overleaf and select main.tex / pdfLaTeX.
The paper uses standard article formatting. A destination's required template,
anonymous-review setting and submission declarations must be applied once a
venue is selected. No publication acceptance or independent review is claimed.
Author: Changyi Wu, Independent Researcher. Contact details supplied by the author:
changyiwu04@gmail.com and hs26971@bristol.ac.uk. No institutional affiliation or
funding is inferred from the email domains.

EVIDENCE AND SCOPE
This paper integrates the original discovery pilot and the separately frozen
A04 follow-up. It does not overwrite earlier reports or pool their results as
one model error rate. No additional model responses were generated while writing
the manuscript. Post-hoc analyses are labelled in the text and saved records.
The synthetic model experiments are distinct from the real SEC metadata audit.
There is no real-holdings PnL result and no claimed new algorithm or theorem.

The source ZIP is sufficient to compile the paper and regenerate its figures:
  python3 make_figures.py
Requires matplotlib and numpy. The precomputed evidence files are included.

The COMPLETE reproducibility ZIP additionally contains two sibling directories:
  disclosure_code_pilot/  raw first answers, prompts, local freezes, fixtures,
                         saved program outputs, original reports and audits
  rule_history/          the 28 public SUBMISSION.tsv tables, download manifest,
                         original data specification and accession-level results;
                         earlier GPT rule-panel prompts, answers and grades
After extracting that full archive, run from submission_paper/:
  python3 verify_evidence.py
This independently rechecks manuscript counts and SEC metadata without running
model-generated programs. It writes evidence/manuscript_verification.json.

For the 9 November revision, also run from submission_paper/:
  python3 revision_checks.py
This independently checks all five realized filing-lag schedules, same-boundary
45-day-floor sensitivity, verbatim model quotations, and the auxiliary GPT QA
denominators. It also checks the opening example's saved execution and independently
confirms 40 of 48 rows delayed in five of six periods; the eight rows in the
day-61 filing period are unchanged. It runs authored reference
policies only, not candidate programs.
Results are saved in evidence/revision_checks_2026-11-09.json.
REVISION_NOTES_2026-11-09.txt records the changes and their evidential scope.
The full archive preserves the 8 November paper under archive/2026-11-08/,
the preceding 10-page evidence revision under archive/2026-11-09-evidence-revision/,
and the preceding 9-page editorial version under archive/2026-11-09-editorial-restructure/.
The preceding layout revision is preserved under archive/2026-11-09-layout-revision/.
The compile-only source ZIP excludes those directories to keep one main.tex entry.

Deeper saved-output audits, without new model calls or candidate execution:
  cd ../disclosure_code_pilot
  python3 audit_saved_results.py
  python3 audit_recovery.py
  python3 audit_full_horizon_saved.py
  cd extensions/A04_form_swap
  python3 audit_saved.py
  python3 audit_capture.py
These original scripts may refresh their audit timestamps. Preserve a copy if
byte-for-byte comparison against the package's original hashes is required.

Do not execute or import generated candidate source directly on the host.
Rerunning candidate programs requires the isolated runtime described in the
original project's README and A01 amendment. Verification of saved outputs
does not reproduce the commercial model generations themselves.

The full archive preserves prior protocol and report versions as provenance;
main.tex is the current integrated manuscript. Historical text can differ from
later corrections, which are explicitly identified in the current paper.
Package hashes are supplied in MANIFEST_SHA256.json at archive root.
