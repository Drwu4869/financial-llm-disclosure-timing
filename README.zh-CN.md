# 金融文本、投资组合穿透与披露时点研究

这里不只有最后一篇论文。文本碎片化、投资组合风险、暴露计算与穿透、聚合诊断公式、推理复验、部分披露和原始报告阅读，都已展开为独立研究板块。

**[进入完整研究合集](research/README.zh-CN.md)** · [English research collection](research/README.md) · [完整探索历程](docs/research-journey.zh-CN.md)

各板块可直接查看原始代码、数据、模型回答和 LaTeX 推导；旧论文原稿继续保留，后来修正或不支持原结论的实验放在旁边一起看。

---

# 不偷看未来，也可能用错数据

**No Look-Ahead, Yet Too Late: Inapplicable Disclosure Rules in LLM-Generated Backtest Code**  
Changyi Wu · Independent Researcher · 2026 年 11 月 9 日工作论文

[英文首页](README.md) · [论文 PDF](paper/main.pdf) · [LaTeX](paper/main.tex) · [Word](paper/No_Look_Ahead_Yet_Too_Late.docx) · [完整研究历程](docs/research-journey.zh-CN.md)

这项研究最后发现的问题很具体：**模型写出的回测代码没有提前使用未来数据，却把已经公开的持仓额外扣住，等到报告期末第 60 天才允许使用。** 在指定的历史时期，这条公开时间规则并不适用。

## 最终拿到了什么证据

| 检验 | 结果 | 能说明什么 |
| --- | --- | --- |
| 最初 GPT 带日期的普通提示/防前视提示 | 12 份程序中 10 份设置了 60 天地板 | 不是“申报后再加 60 天”，而是取申报日与期末加 60 天中的较晚者 |
| 单独冻结的 N-PORT 复验 | GPT 5/6，Claude 2/6 命中预定的 60 天规则 | 另两份 Claude 程序符合事后发现的交易/申报日历变体，单独报告 |
| 换成 13F | 12 份程序均未设置 45 天地板 | 不支持“模型普遍把所有申报截止日当公开日”的强解释 |
| 明确规定公开日期语义 | 后续研究的 12 份 P2 程序全部匹配参考实现 | 明确的数据契约在这些案例上有效 |
| 349,673 份真实 SEC 申报元数据 | 假设使用 60 天地板，85.93% 会被延后，整体平均 4.13 天 | 测得的是信息等待时间，不是收益损失 |

最有价值的结论是：**只检查有没有“偷看未来”不够，还要检查有没有错误地丢掉当时已经能用的信息。** 代码能运行、没有前视偏差，也不等于实现了正确的金融含义。

## 为什么把探索过程也放出来

最开始研究的是“同一笔投资写成多个产品后，模型会不会误以为更分散”。后来发现，小模型结果受到提示词示例数字影响；重新归一化的几次成功可能只是碰巧。再后来，开启推理的配置几乎消除了旧的计算错误，强模型也答对了已观察到的干净持仓区间题。

这些结果促使研究继续缩小问题：从答案是否算对，到信息是否完整，再到该用哪一天公开的资料，最后测试模型把什么规则写进可执行代码。这个过程中的负结果、失败的诊断方法和纠正过的计分，都值得保留。

- [研究历程：每次为什么转向](docs/research-journey.zh-CN.md)
- [决定记录：保留什么、停止什么](docs/decision-log.md)
- [证据与结论对应表](docs/claim-ledger.md)
- [从业者可使用的检查清单](docs/practitioner-checklist.md)
- [历史稿、报告、实验包索引](docs/artifact-index.md)
- [尚未完成的下一步问题](docs/open-questions.md)

旧稿是研究档案，不是与当前论文并列的多篇已发表成果。尤其是 22 页 v5、32 页 v8 的小模型结论，需要与后来的推理复验一起看。所有新写的研究历程都标明是 **11 月 9 日的回顾整理**，不会冒充当时的预注册记录。

## 如何复查

```bash
python3 tools/check_release.py
python3 tools/reproduce_current.py --output /tmp/disclosure-timing-verification
```

这些命令核查保存的材料，不重新请求模型，也不直接执行模型生成的程序。详细说明见[复现指南](docs/reproduction.md)。

本项目仍是工作论文，尚不等于录用或独立同行评审。作者：Changyi Wu，Independent Researcher。联系：changyiwu04@gmail.com / hs26971@bristol.ac.uk。
