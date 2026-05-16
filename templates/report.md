# 通用调研报告模板（6 段式）

适用：market / general / user-research / talent-research / trend-foresight / 任何不需要特殊模板的调研。

引用规范：内联 markdown 超链接 + 末尾 References（gpt-researcher 风格，APA 7th）。

---

## 模板（直接套）

```markdown
# {调研主题}

> **范围**：{时间窗 / 地区 / 目标读者}
> **深度**：{light / full / deep}
> **完成时间**：{YYYY-MM-DD}
> **总源数**：{N}（Tier A: x / B: y / C: z / D: w）

---

## TL;DR

{3-5 句话。必须包含：}
- {1 个最关键结论}
- {1 个最反直觉发现}
- {1 个明确建议}

---

## 1. 关键发现 (Key Findings)

{3-7 条最重要的发现，每条 100-300 字。}
{每条结构：}

### 1.1 {发现标题（结论式陈述）}

**Finding**：{结论}

**Evidence**：
- {证据 1} ([source title](url), Tier B, 2024-08)
- {证据 2} ([source title](url), Tier A, 2025-02)
- {证据 3} ([source title](url), Tier B, 2024-12)

**Inference**：{我从证据推出的判断（明确标注是 inference 不是 fact）}

**反方观点**：{反方 / 不同视角的论据}（[source](url)）

### 1.2 {下一个发现}
...

---

## 2. 详细分析 (Detailed Analysis)

按子问题展开。每个子问题作为一个 `##` 标题。

### 2.1 {子问题 1 标题}

{完整论述，2-5 段。}
{每段都要有 ≥1 个内联引用。}
{表格、列表、数据可视化按需穿插。}

### 2.2 {子问题 2 标题}
...

---

## 3. 影响 (Implications)

{基于 findings，对不同利益相关者意味着什么。}

**对 {读者类型 A}（如：产品经理）**：
- {含义 1}
- {含义 2}

**对 {读者类型 B}（如：投资人）**：
- ...

---

## 4. 风险与不确定性 (Risks & Uncertainties)

### 4.1 已识别风险
| 风险 | 可能性 | 影响 | 缓解方向 |
|------|-------|------|---------|
| {风险 1} | 高/中/低 | 高/中/低 | {action} |

### 4.2 信息冲突
{Phase 5 显式标注的冲突。}
- **冲突 N**：关于 X，源 A 说 Y，源 B 说 Z。我的判断：...（理由：...）

### 4.3 研究限制
- {哪些子问题没充分回答}
- {哪些信源缺位}
- {数据时效问题}

---

## 5. 建议 (Recommendations)

{必须是可执行的，不允许空洞结论。}

1. **{Action 1}**：{具体怎么做} — 基于 finding {N}
2. **{Action 2}**：...
3. **{Action 3}**：...

**监控指标**（用户后续可持续关注的）：
- {Metric 1}：{触发阈值}
- {Metric 2}：...

---

## 6. References

按 APA 7 格式，每条带 URL。

```
1. Author, A. (2024, August 15). Title of article. Publication Name. https://example.com/article
2. Smith, J., & Doe, R. (2025, February 3). Title of paper. *Journal Name*, *Volume*(Issue), pages. https://doi.org/...
3. 作者. (2024). 中文文章标题. 媒体名. https://example.cn
4. Company X. (2024, December 1). Press release title. https://...
5. ...
```

---

## 附录（可选）

### A. 子问题清单（来自 plan.md）
{展示研究 plan 给用户看研究思路}

### B. 研究 transparency log
- 总 web 调用次数：N
- 关键决策日志：参考 gap-log.md
- 4 个 critic finding 总结
```

---

## 写作规范（硬约束）

### Citation 规范
1. **内联引用**：`([source title](url))` 形式
2. **末尾 References**：APA 7th + 必须带 URL（即便是论文，arXiv / DOI 都行）
3. **同一来源多次引用**：每次都引（不用"同上"），保持可点击
4. **来源元数据**：在内联引用后用括号标注 Tier 和日期，如 `([source](url), Tier B, 2024-08)`

### Markdown 风格
- 标题严格 `#` / `##` / `###` 三层（不要 4 层以上）
- **不要** Table of Contents（gpt-researcher 风格）
- 表格用 markdown 标准表格
- 关键数字用 **bold**
- 引用用户原话或专家原话用 `>` blockquote

### 字数与篇幅
- Light tier：1500-3000 字
- Full tier：5000-10000 字
- Deep tier：10000-20000 字
- TL;DR 必须 ≤500 字，独立可读

### 反幻觉
- 任何引用必须能 `WebFetch` 验证（跑 `scripts/verify_citations.py`）
- 不可验证的数据 → 改写为"约 / 据传 / 公开未披露"
- 模糊数字（如 "数百万"）必须找精确版本

### 标签使用
- 在关键 claim 前加 inline 标签明确性质：
  - `**[Fact]**` — 可验证事实
  - `**[Inference]**` — 我的推断
  - `**[Recommendation]**` — 行动建议
  - `**[Open]**` — 未答 / 待验证
- 这是 pytrak89 五原则之一，必须遵守
