# Original reports versus cleaned financial tables

**中文：原始财报/基金报告阅读。** 清洗好的表格太容易，是否换成数百页 PDF 就能暴露模型问题？这个方向保留原始资料来源、PDF 与文本配对题、全部回答和结果。

## Design

A feasibility pilot used a **510-page BlackRock annual report**, later factsheets, and matched extracted text. Four original-PDF trials were compared with four text trials on exposure and limit decisions. The scenarios also checked whether a precise earlier holding was incorrectly carried into a later incomplete disclosure.

## Observed outcome

GPT-6 High returned correct exposure, limit decision and source-page evidence in **all four PDF and all four text trials**. It did not substitute the older precise holding for the later partial information in these cases.

This was a commercial product workflow, with internal retrieval/tool use unobserved, one issuer/account and three distinct exposure targets. The eight responses are not eight independent documents. The result does not prove general long-document competence, historical public availability or broad model equivalence.

## Why it belongs in the research portfolio

It records a real attempt to make the task realistic, and the resulting negative signal. Adding pages did not create the anticipated failure in these sampled cases. That helped move attention toward which rule and which date govern availability, rather than increasing document length without a discriminating hypothesis.

Original issuer reports are identified in [sources.json](sources.json); the already published package contains the retained evidence and text inputs. It is not a claim that every full original PDF is redistributed here.

## Browse every answer

| Case | PDF response | Matched-text response |
| --- | --- | --- |
| A | [A PDF](A_pdf.answer.json) | [A text](A_txt.answer.json) |
| B | [B PDF](B_pdf.answer.json) | [B text](B_txt.answer.json) |
| C | [C PDF](C_pdf.answer.json) | [C text](C_txt.answer.json) |
| D | [D PDF](D_pdf.answer.json) | [D text](D_txt.answer.json) |

[Protocol](protocol.json) · [Questions](questions.json) · [Answer key](answer_key.json) · [Item scores](case_scores.csv) · [Original scorer](original_verify.py) · [Report](../../archive/reports/BlackRock_Original_PDF_Pilot.pdf) · [Complete evidence](../../archive/packages/BlackRock_Original_PDF_Pilot_Evidence.zip).

## Files, provenance and reproduction

The files beside this README are byte-for-byte browsing copies of the previously published archives. Some original scripts depend on their original directory layout: use the complete package for execution, or run the repository-level historical reproduction command below. Filenames were shortened for navigation; their original paths and hashes are in [the source map](../source-map.json). The complete archives preserve additional prompts, raw outputs, protocols, manuscripts and supporting files.

```bash
python3 tools/reproduce_historical.py
```

Run that command from the repository root with NumPy and SciPy installed. It checks archived evidence and reference arithmetic, without making model requests. This navigation and commentary were added retrospectively on 9 November 2026; they are not new experiments or a new preregistration. These topics overlap and must not be counted as independent studies or accepted publications.
