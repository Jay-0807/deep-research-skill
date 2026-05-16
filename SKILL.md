---
name: deep-research
description: 通用深度调研技能。当用户需要做调研、研究、竞品分析、市场分析、行业研究、技术选型、公司尽调、用户研究、人才/招聘调研、趋势前瞻、学术综述、写研究报告时触发。支持 8 大场景路由 + 1 个通用骨架，自动选择信源管道（中英文）和报告模板。Trigger when user asks for research, competitive analysis, market analysis, due diligence, tech evaluation, user research, talent research, trend analysis, literature review, or any deep investigation that requires multi-source synthesis with citations. 触发关键词包括（但不限于）："调研"、"研究"、"分析"、"对比"、"梳理"、"评估"、"尽调"、"竞品"、"市场"、"趋势"、"benchmark"、"research"、"investigate"、"analyze"、"compare"、"deep dive"、"landscape"。
---

# Deep Research — 通用深度调研

## 这个 skill 解决什么问题

用户提出一个"调研类"诉求时，本 skill 提供一套完整的研究流水线：**识别场景 → 选方法论 → 选信源 → 多源检索 → 信息提取 → 冲突标注 → Knowledge Gap 循环 → 综合写作 → 对抗式 critique → 引用校验 → 结构化输出**。

设计参考了 `hyperresearch`（DeepResearch-Bench RACE 第一）、`199-bio` 的引用校验、`gpt-researcher` 的引用规范、Stanford `STORM` 的视角发现、Anthropic 多 agent research 工程实践、qx-labs `IterativeResearcher` 的 Knowledge Gap 循环。

---

## 五条调研原则（system baseline，每次调用都必须遵守）

1. **每条重要 claim 必须有源** — 没有可验证的来源就不写进报告。把"我推测"和"来源说"严格区分开。
2. **当前数据优先 + 过期数据必须 flag** — 凡使用 2 年前以上的数据，必须显式标注"截至 YYYY 年"，并说明是否已有更新数据。
3. **必须包含反方观点和下行风险** — 默认报告里的每个结论都要附带"反方/质疑"。没有反方说明研究不够深，必须继续找。
4. **转化为可执行决策** — 报告结尾必须有 Recommendation 段，告诉读者"基于以上发现，建议做什么/不做什么"。空洞的结论（"这是一个有前景的领域"）禁止出现。
5. **严格区分 facts / inferences / recommendations** — 用 markdown 标签或分段明确区分这三类内容。Inference 必须标注推理依据。

---

## 工作流（4 步）

### Step 1：场景路由（识别用户 query 属于哪一类）

用户 query 提交时，先做场景分类。8 个主场景 + 1 个通用骨架：

| 场景 | 触发关键词 | 加载文件 |
|------|----------|---------|
| 竞品调研 | 竞品、对手、SWOT、benchmark、positioning、competitive | `scenarios/competitive.md` |
| 市场/行业 | 市场、行业、TAM、规模、增长、value chain、industry | `scenarios/market.md` |
| 学术/论文 | 论文、文献、literature、综述、survey、academic | `scenarios/academic.md` |
| 技术选型 | 选型、技术栈、框架对比、benchmark、tech evaluation | `scenarios/tech-evaluation.md` |
| 公司/尽调 | 尽调、due diligence、公司、估值、投资、融资 | `scenarios/due-diligence.md` |
| 用户/客户 | 用户、客户、JTBD、痛点、用户访谈、user research | `scenarios/user-research.md` |
| 人才/招聘 | 人才、招聘、薪资、候选人、人才地图、talent | `scenarios/talent-research.md` |
| 趋势/前瞻 | 趋势、未来、信号、foresight、trend、emerging | `scenarios/trend-foresight.md` |
| **通用/混合** | 以上都不清晰，或多场景混合 | `scenarios/general.md` |

**组合调用**：很多真实需求是多场景的，例如：
- "调研中国 AI Agent 创业公司" = `competitive.md` + `due-diligence.md` + `market.md`
- "GPT-5 vs Claude 4.7 哪个更适合做 agent" = `tech-evaluation.md` + `academic.md`
- "Z 世代为什么不喜欢小红书" = `user-research.md` + `trend-foresight.md`

**路由动作**：
- Read 选中的 scenario 文件（1-3 个）
- 把场景特定的方法论、信源、模板提示注入到后续推理

### Step 2：套用通用骨架（8 阶段流水线）

Read `methodology/pipeline.md`，按 8 阶段执行：

```
Phase 1  澄清     ─ 主动反问 + canonical query 写入 ./research-vault/query.md
Phase 2  拆解     ─ STORM perspective discovery + Anthropic 四件套委派
Phase 3  检索     ─ 多源并行（按 scenario 选择 sources/）
Phase 4  提取     ─ 摘要 + 来源可信度评分（source-tiers）
Phase 5  冲突标注  ─ 显式 surface 矛盾源，不让 LLM 静默融合
Phase 6  Gap 循环  ─ Knowledge Gap Agent 决定是否继续 + 双层停止
Phase 7  综合     ─ outline-first + section-by-section + patch-never-regenerate
Phase 8  Critique ─ 4 个对抗式 critic + 引用校验脚本
```

阶段细节在 `methodology/pipeline.md`。复杂调研必须按这 8 阶段走，简单调研可跳过 Phase 5/6/8 中的部分子步骤（但 Phase 1/2/3/4/7 不可省）。

### Step 3：选信源 + 选模板

根据 Step 1 选中的 scenario 文件里的"推荐信源"和"推荐模板"指引：

**信源管道**（中英文同等覆盖）：
- `sources/academic.md` — 学术：Semantic Scholar、arXiv、OpenAlex、CrossRef、PubMed、知网、万方
- `sources/industry.md` — 行业：Statista、IBISWorld、Gartner、IDC、艾瑞、亿欧、36氪、IT 桔子、头豹
- `sources/company.md` — 公司：SEC EDGAR、Crunchbase、PitchBook、企查查、天眼查、启信宝
- `sources/general-web.md` — 通用 web：Google、Bing、Brave、Tavily、Serper、Exa、Jina、Firecrawl

**报告模板**：
- `templates/report.md` — 通用 6 段式（Exec / Findings / Implications / Risks / Reco / Sources）
- `templates/competitive-matrix.md` — 竞品对比表 + 定位地图
- `templates/due-diligence-memo.md` — 投资备忘录格式
- `templates/academic-review.md` — Wikipedia/综述风格

### Step 4：校验（自动 / 手动二选一）

报告草稿完成后必须校验三件事：**信源可信度 / 引用可访问性 / 报告结构硬约束**。

**首选：跑 Python 脚本**（需要 `python ≥3.10` + `pip install requests beautifulsoup4`）：

```bash
python scripts/source_evaluator.py ./research-vault/sources.json    # 信源可信度评分
python scripts/verify_citations.py ./research-vault/report.md       # URL/DOI 可访问性 + 反幻觉
python scripts/validate_report.py ./research-vault/report.md        # 9 项硬约束
```

**回退：如果用户环境无 Python**（在 Windows 上常见），按以下手动 checklist 走一遍：

- 信源可信度：参照 `methodology/source-tiers.md` 的 Tier A/B/C/D 分类规则，人工判定每条 source。要求 Tier A+B ≥ 3，Tier C ≤ 50%，Tier D ≤ 20%
- 引用可访问性：用 WebFetch 抽查 ≥3 条关键引用 URL，验证可访问且页面标题与引用文本大致匹配
- 报告结构：按 `scripts/validate_report.py` 顶部注释里列出的 9 项硬约束逐条 check（也可直接 Read 这个文件查看 check 列表）

**任一校验失败都必须修复后再交付**。校验通过才能向用户呈现最终报告。

---

## 默认输出目录结构

每次调研在工作目录下创建 `research-vault/`：

```
research-vault/
├── query.md              # canonical query（用户原 prompt + 澄清后的细化版）
├── plan.md               # 子问题拆解 + outline
├── sources.json          # 所有引用来源（含可信度评分）
├── findings/             # 阶段性 findings（按子问题）
│   ├── sub-q1.md
│   └── ...
├── conflicts.md          # 冲突信息显式记录
├── report.md             # 最终报告（默认 markdown）
├── report.html           # 可选：HTML（McKinsey 风格）
└── report.pdf            # 可选：PDF
```

vault 设计借鉴 hyperresearch：**Markdown 是真相之源，跨 session 可复用**。后续调研可以 Read 既有 vault 来增量更新而非从零开始。

---

## 何时**不要**用这个 skill

- 用户只是问一个简单事实（"X 公司今年收入多少"）— 直接 WebSearch 一次给答案即可
- 用户要写代码 / 写文档 / 写邮件 — 不是调研
- 用户已经把信源都给齐了，只是让你整理 — 用一般阅读和总结即可
- 用户在让你做 brainstorm / 创意 — 不是验证型研究

判断标准：**是否需要从未知信源做多源交叉验证 + 形成可执行结论**。是 → 用本 skill；否 → 不用。

---

## 与用户的初次交互（必做）

收到调研需求后，**先输出 3 件事再开干**：

1. **场景判定**：我识别这是「场景X + 场景Y」类调研
2. **澄清问题**（1-3 个最关键的）：例如"研究范围只限国内还是全球？"、"时间窗口是过去 1 年还是 3 年？"、"目标读者是投资人/产品经理/技术决策者？"
3. **预估深度**：light tier（30-45 min，~5-10 源）还是 full tier（1.5-2.5h，30-60 源）？

用户回应后再 enter Step 2。
