# Reproduction guide

There are three different activities: verifying distributed files, recomputing results from saved evidence, and collecting or executing new model outputs. This release supports the first two. It does not promise an identical fresh commercial-model run.

## 1. Check the release

From the repository root, with Python 3.11 or later:

```bash
python3 tools/check_release.py
```

This standard-library check verifies SHA-256 hashes and key saved counts. It does not prove that an original experiment was independently replicated. If you edit a file after checkout, the release checksum is expected to change.

## 2. Recompute the current manuscript evidence

Use a new or empty output directory with approximately 650 MB free disk space:

```bash
python3 tools/reproduce_current.py --output /tmp/disclosure-timing-verification
```

The script verifies and extracts `archive/packages/Disclosure_Timing_Public_Evidence.zip`, preserving its sibling directory structure. It then runs:

```bash
cd /tmp/disclosure-timing-verification/submission_paper
python3 verify_evidence.py
python3 revision_checks.py
```

The first checks model-study counts and all 28 raw SEC SUBMISSION tables, exclusions, accession-level lags, and waiting calculations. The second checks realized fixture lags, 13F floor sensitivity, source quotations, preceding rule-question denominators, and the 40/48-row opening example. It evaluates authored reference policies, not candidate source. These scripts use the Python standard library and may refresh generated verification files in the extraction directory.

The expected results include 36 follow-up programs, 349,673 eligible accessions, 2,095 follow-up filing interventions with no numerical witness, and 65 inconclusive intervention refusals. The archive preserves historical-period and full-cohort summaries separately.

## 3. Deeper saved-output audits

Within the extracted tree:

```bash
cd disclosure_code_pilot
python3 audit_saved_results.py
python3 audit_recovery.py
python3 audit_full_horizon_saved.py
cd extensions/A04_form_swap
python3 audit_saved.py
python3 audit_capture.py
```

These are original authored audit scripts. They read preserved outputs and verify relevant frozen, candidate-source, and output hashes; they do not make new model calls. Some refresh audit timestamps, so keep the distributed archive unchanged if you need byte-level comparison. `audit_capture.py` compares Claude source copies with preserved whole-message copies; operational browser accessibility dumps are not required.

The public export retains scientific source/output bytes but omits operational browser traces and redacts private session URLs. Original whole-package manifests can therefore mention files absent from the export; the public release manifest and export ledger document that distinction. Do not interpret an intentionally omitted browser trace as an absent model response.

## 4. Build the current paper

The browsable `paper/` directory corresponds to `submission_paper/` inside the archive. A normal TeX Live or MiKTeX installation can compile it:

```bash
cd paper
bash build.sh
```

`main.bbl` is included as a fallback bibliography. Regenerating figures with `python3 make_figures.py` also requires NumPy and Matplotlib. The precompiled PDF, figures, and Word conversion are already supplied. The manuscript-verification scripts in `paper/` expect the evidence siblings; run them inside the extracted package as above.

## 5. Historical stages

See the [artifact index](artifact-index.md). Each older ZIP has its own root layout and README. In particular:

- v5 contains the conditional mathematics, diagnostic evaluation, and motivating pilot archive.
- v9 contains the portfolio exposure integration and nested prior evidence packages; it must be interpreted with the reasoning recheck.
- The reasoning recheck contains 100 frozen evaluation responses and separate development records.
- Top-ten hosted evidence distinguishes first answers from technical recoveries and preserves the scoring amendment.
- Original-PDF, temporal-disclosure, and holiday-pair packages are separate pilots, not extra independent replications of the final code study.

No new exhaustive revalidation of every historical theorem or every old score was performed for this GitHub export. The research narrative cites the saved stage reports and labels their scope.

## Collecting or executing new outputs

Do not import or execute generated candidate source directly on a host containing credentials or personal files. The original study uses an isolated runtime with restricted filesystem, network, and subprocess access; its instructions are in the extracted pilot README and runtime amendment. The convenience scripts here do not invoke that execution path.

Fresh runs would need recorded product settings, new first-response logs, and explicit handling of backend changes and technical missingness. They are new evidence, not a byte-for-byte reproduction of the original generation.
