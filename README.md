# Firefly Deep Research Skill 萤火深度调研

A comprehensive deep-research skill for Claude Code that routes user research queries across **8 specialized scenarios + 1 generic skeleton**, applies a battle-tested 8-stage research pipeline, and produces decision-grade reports with bilingual (Chinese + English) source pipelines and automated citation validation.

为 Claude Code 设计的通用深度调研技能：识别 8 大调研场景 + 1 个通用骨架，套用 8 阶段研究流水线，输出可执行的决策级报告，中英文信源对等覆盖，含 Python 引用校验脚本。

---

## Why this skill / 为什么有这个 skill

Existing Claude skills do research either narrowly (single scenario like `competitive-analyst`) or shallowly (one-size-fits-all `deep-research` without scenario specialization). This skill fills three structural gaps in the ecosystem:

现有 Claude 生态里的调研类 skill 要么场景单一，要么大而化之。本 skill 填补三个空白：

1. **Scenario router + template composition** — no major project does "classify first, then dispatch to the right methodology"; this skill routes across 9 scenarios and lets them combine (e.g. *"research Chinese AI Agent startups"* = `competitive` + `due-diligence` + `market`).
2. **Three under-served scenarios** — `tech-evaluation`, `user-research`, and `talent-research` are essentially absent in the open-source skill ecosystem; this skill ships dedicated SOPs for each.
3. **Bilingual source pipelines** — most projects default to English-only academic / industry sources; this skill ships parallel coverage of Chinese sources (知网, 艾瑞, 头豹, 企查查, etc.) at equal depth.

---

## What's inside / 包含什么

```
firefly-deep-research-skill/
├── SKILL.md                          # 主入口：场景路由 + 五原则 + 4 步工作流
├── methodology/                      # 跨场景共用方法论
│   ├── pipeline.md                   #   8 阶段流水线
│   ├── source-tiers.md               #   信源 4 级分层规则
│   ├── critique-loop.md              #   4 个对抗式 critic
│   └── stopping-criteria.md          #   Knowledge Gap + 双层停止
├── scenarios/                        # 8 大场景 + 1 个通用骨架
│   ├── competitive.md                #   竞品调研
│   ├── market.md                     #   市场/行业
│   ├── academic.md                   #   学术/论文
│   ├── tech-evaluation.md            #   技术选型 ⭐填空白
│   ├── due-diligence.md              #   公司/尽调
│   ├── user-research.md              #   用户/客户 ⭐填空白
│   ├── talent-research.md            #   人才/招聘 ⭐填空白
│   ├── trend-foresight.md            #   趋势/前瞻
│   └── general.md                    #   通用/混合
├── sources/                          # 信源管道（中英对等）
│   ├── academic.md                   #   Semantic Scholar/arXiv + 知网/万方
│   ├── industry.md                   #   Gartner/IDC + 艾瑞/头豹/亿欧/36 氪
│   ├── company.md                    #   SEC/Crunchbase + 企查查/天眼查
│   └── general-web.md                #   Google/Bing/Tavily/Jina
├── templates/                        # 报告输出模板
│   ├── report.md                     #   通用 6 段式
│   ├── competitive-matrix.md         #   竞品矩阵 + 定位地图
│   ├── due-diligence-memo.md         #   投资 IC Memo
│   └── academic-review.md            #   综述 + taxonomy
└── scripts/                          # 校验脚本（Python，可选）
    ├── verify_citations.py           #   URL/DOI 反幻觉
    ├── validate_report.py            #   9 项硬约束
    └── source_evaluator.py           #   信源自动打分
```

---

## Install / 安装

### Option 1 — Clone into Claude skills directory

```bash
# macOS / Linux
git clone https://github.com/Jay-0807/firefly-deep-research-skill.git ~/.claude/skills/firefly-deep-research-skill

# Windows PowerShell
git clone https://github.com/Jay-0807/firefly-deep-research-skill.git $HOME\.claude\skills\firefly-deep-research-skill
```

### Option 2 — Project-level install

```bash
cd <your-project>
mkdir -p .claude/skills
git clone https://github.com/Jay-0807/firefly-deep-research-skill.git .claude/skills/firefly-deep-research-skill
```

### Optional — install Python deps for the validation scripts

The skill works without Python; it falls back to a manual checklist. To enable automated validation:

```bash
pip install requests beautifulsoup4
```

---

## How to trigger / 怎么触发

In any Claude Code session, ask a research-style question. The skill auto-loads on keywords like:

- 调研 / 研究 / 分析 / 对比 / 梳理 / 评估 / 尽调 / 竞品 / 市场 / 趋势 / benchmark
- research / investigate / analyze / compare / deep dive / landscape

Example prompts:

- "调研一下中国具身智能领域的创业公司"
- "对比 LangGraph 和 Pydantic AI，做技术选型"
- "做一份小红书 Z 世代用户的调研"
- "深度尽调一下 Anthropic 这家公司"
- "AI Agent 这个赛道未来 3 年的趋势"

You can also explicitly invoke: *"用 firefly-deep-research-skill 调研 X"*.

---

## How it works / 工作流

Every research run follows 4 steps:

### Step 1 — Scenario routing

The skill classifies the query into one or more of 9 scenarios. Multi-scenario queries (e.g. *"competitive landscape + due diligence"*) load multiple scenario files and combine their methodologies.

### Step 2 — Apply the 8-stage pipeline

```
Phase 1  澄清     ─ 主动反问 + canonical query 持久化
Phase 2  拆解     ─ STORM perspective discovery + Anthropic 四件套委派
Phase 3  检索     ─ 多源并行 + 学术 API 优先
Phase 4  提取     ─ 来源可信度评分 (Tier A/B/C/D)
Phase 5  冲突标注  ─ 显式 surface 矛盾源（不静默融合）
Phase 6  Gap 循环  ─ Knowledge Gap Agent + 双层停止
Phase 7  综合     ─ outline-first + patch-never-regenerate
Phase 8  Critique ─ 4 个对抗 critic + gap-fetch
```

### Step 3 — Choose sources + template

Picks 2–4 source pipelines (from `sources/`) and the right report template (from `templates/`) based on the active scenario(s).

### Step 4 — Validate

Runs the 3 Python validation scripts (or falls back to a manual checklist if Python isn't available). Validation failures must be fixed before delivery.

---

## Output / 产出

Every research run creates a `./research-vault/` directory in the caller's working directory:

```
research-vault/
├── query.md              # canonical query (用户原 prompt + 澄清后的细化版)
├── plan.md               # 子问题拆解 + outline
├── sources.json          # 所有引用来源（含可信度评分）
├── findings/             # 阶段性 findings
├── conflicts.md          # 显式记录冲突信息
├── gap-log.md            # 每轮 Knowledge Gap 决策日志
├── critique.md           # 4 个 critic 的 findings
└── report.md             # 最终报告（可附加 report.html / report.pdf）
```

The vault is reusable across sessions — subsequent research can incrementally extend an existing vault.

---

## Five principles / 五条原则

Every report obeys:

1. **Every meaningful claim must have a source** — no claim → no source → not in the report.
2. **Current data first, stale data must be flagged** — data >2 years old gets explicitly marked.
3. **Counter-arguments and downside risks are mandatory** — no opposing view = research not deep enough.
4. **Findings must convert to actionable recommendations** — no empty conclusions ("有前景的领域") allowed.
5. **Strictly separate facts / inferences / recommendations** — inference must state its evidence.

---

## Differentiation / 差异化

| Dimension | This skill | Most existing skills |
|-----------|-----------|---------------------|
| Scenario coverage | 9 specialized + composable | 1–8 monolithic |
| Tech-evaluation / user-research / talent-research SOPs | ✓ ⭐ | rare or absent |
| Chinese sources (知网/艾瑞/企查查/...) | ✓ equal weight | usually English-only |
| Scenario router | ✓ (auto + manual combine) | none |
| Source tiering (A/B/C/D) | ✓ with auto-scoring script | typically vague prompt-level |
| Conflict surfacing | ✓ explicit in report | usually silently merged |
| Citation hallucination check | ✓ Python script | rare |
| Patch-never-regenerate | ✓ critic + patcher tool lock | rare |

---

## Acknowledgments / 致谢

The skill synthesizes ideas from:

- [hyperresearch](https://github.com/jordan-gibbs/hyperresearch) — 16-step pipeline, patch-never-regenerate, SQLite vault concept
- [199-biotechnologies/claude-deep-research-skill](https://github.com/199-biotechnologies/claude-deep-research-skill) — 9-item validation checklist, citation verification, three-format output
- [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) — APA citation format, inline markdown hyperlink convention
- [Stanford STORM](https://github.com/stanford-oval/storm) — perspective discovery for question decomposition
- [Anthropic's Multi-Agent Research blog](https://www.anthropic.com/engineering/multi-agent-research-system) — lead-agent four-item delegation (objective/format/tools/boundaries)
- [qx-labs/agents-deep-research](https://github.com/qx-labs/agents-deep-research) — Knowledge Gap Agent for dynamic stopping
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) — modular scenario templates (competitive / market / trend / data-research)
- [pytrak89/everything-claude-code-v2](https://github.com/pytrak89/everything-claude-code-v2) — decision-driven five-principle baseline

---

## License

[MIT](LICENSE)

---

## Contributing

Issues and PRs welcome. Particularly interested in:

- Additional Chinese source pipelines (especially CN academic, finance, healthcare verticals)
- Scenario-specific templates for verticals not yet covered (legal, IP, regulatory)
- Better automated source-tier scoring (current implementation uses static domain whitelists)
- Real-world report examples (anonymized) for any of the 9 scenarios

If you build on this skill or use it for a substantial project, a star ⭐ is appreciated.
