# Checklist for disclosure-based backtests

This is an engineering interpretation of the observed study, not a validated production standard. The successful explicit-contract condition motivates the checks; their general deployment effectiveness remains untested.

## Data contract

- **Identify the rule version.** Record form, reporting entity category, historical effective interval, primary source, exceptions, and postponements.
- **Separate timestamps.** Distinguish report period, submission start, acceptance, actual public availability, amendment availability, decision time, and trade execution time.
- **Give columns precise meanings.** A raw submission timestamp and a public-availability timestamp are not interchangeable. A field named `filing_date` needs a documented convention.
- **Fix the boundary once.** Specify timezone, date-only handling, holiday calendar, inclusive/strict eligibility, and mapping to the next execution session.
- **Keep revisions point-in-time.** Selecting the last revision across the complete dataset can introduce later information into earlier decisions.

## Tests that distinguish plausible policies

| Input/control | Failure it can reveal |
| --- | --- |
| Filing earlier than a report-period deadline | Unnecessary waiting until the deadline |
| Filing later than that deadline | Premature use by a fixed report-period lag |
| Same period with a later amendment | Full-history revision overwrite |
| A decision on the public day and on the following day | Inclusive/strict boundary mismatch |
| Final decision with a valid next execution session | An interface failure mistaken for financial abstention |
| Missing public date with alternative admissible release histories | Unsupported certainty about an unidentified date |
| Paired examples on either side of a real rule change | Applying the wrong regime to the historical period |

Check both (a) whether changing unavailable information changes an earlier output and (b) whether the output matches the requested policy when information **is** available. A cash-only strategy or a maximum-based embargo can pass the first test and fail the second.

## How the paper implements the contrast

The controlled task requests a fixed signal. A supplied public filing date is the reference; a candidate may instead use the later of that date and period end plus 60 days. The evaluator compares daily portfolio weights against authored policies. It does not infer timing from Sharpe ratios or claim to measure real economic loss.

The follow-up's filing dates are already adjusted for the stated after-hours convention. It does not test whether models can derive those dates from raw transmission timestamps. Shifting an already-adjusted date again would create a different error.
