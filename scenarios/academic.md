# 场景：学术 / 论文调研 (Academic / Literature Review)

## 何时触发
用户问："X 领域有哪些论文"、"X 的文献综述"、"X 的研究进展"、"X 的 SOTA"、"X 方向的奠基论文"、"找一篇关于 X 的 survey"。

## 必答 5 大问题

1. **奠基论文**：这个领域的 3-10 篇 seminal papers（必读经典）
2. **当前 SOTA**：过去 18 个月的 top venues 论文 + 最佳性能/方法
3. **研究流派**：主要技术路线 / 学派 / 阵营划分
4. **公认 gap**：领域内公认的未解决问题
5. **方法论**：常用 benchmark / dataset / 评测方法

## 推荐方法论

### 1. STORM Perspective Discovery（必做）
按 `methodology/pipeline.md` 的 Phase 2 策略 A：
- 先找 ≥2 篇这个领域已有的 survey / review paper（用 "X survey" / "review of X" 搜）
- 提取这些 survey 的 outline 和 taxonomy
- 用它们的视角作为子问题骨架

不做这一步直接拍脑袋拆解，会漏掉学界公认的分类轴。

### 2. 引文链溯源（Citation Chain）
- 从 1-2 篇核心论文出发
- 追"它引用了谁"（backward citation）→ 找到奠基论文
- 追"谁引用了它"（forward citation，Semantic Scholar / Google Scholar 都有）→ 找到后续发展
- 通常 3 跳之内能覆盖一个 sub-topic 的核心文献

### 3. 多 API 互补检索
**不要只用 Google Scholar**（被 ban 风险高、API 受限）。组合使用：
- **Semantic Scholar API**：免费、可批量、含引用图（最推荐）
- **arXiv API**：preprint 最快、ML/CS 领域最全
- **OpenAlex**：开放学术图谱，可替代 Scopus
- **CrossRef**：DOI 解析
- **PubMed**：生医必用
- **中文学术**：知网（CNKI）、万方、维普、国家科技图书文献中心

### 4. 论文质量评估
不是所有论文都同等重要：
- **顶会 / 顶刊** + **高引用**（>100 引用，时间 normalize）= must-read
- **新论文**（<1 年）：引用不足以判断，看 venue + author + 是否被几个 follow-up 引用
- **arXiv-only preprint**：可读但要小心未经同行评议
- **会议口头报告 vs poster**：口头更重要

### 5. Novelty 评估（来自 lingzhi227/agent-research-skills）
对每篇论文回答 3 个评分：
- **Interestingness**：是否提出了非直觉的发现 / 重要的问题
- **Feasibility**：方法是否可复现 / 资源是否合理
- **Novelty**：相对于已有工作的新颖度

## 推荐信源
- 主要：`sources/academic.md`
- 英文优先级：Semantic Scholar > arXiv > OpenAlex > CrossRef > Google Scholar
- 中文：知网 / 万方 / 维普
- 工程类：GitHub（找官方实现） + Papers with Code（找 SOTA leaderboard）

## 推荐模板
`templates/academic-review.md`（Wikipedia/综述风格）

## 输出 deliverables
1. **Introduction**：领域定义 + 重要性 + 综述范围
2. **Background / Foundations**：奠基论文 + 关键概念
3. **Taxonomy**：研究分类（按方法 / 任务 / 应用）
4. **State of the Art**：当前 SOTA 各方向的代表工作
5. **Methods Comparison**：表格对比（method × dataset × metric）
6. **Open Problems**：公认 gap + 潜在方向
7. **References**：APA 或 BibTeX 格式

字数：综述至少 5k 字，要点报告 2-3k 字。

## 反模式
- 只列论文清单，不做 taxonomy → 用户拿到一堆名字不知道关系
- 引用都是 arXiv preprint，没有顶会论文 → 必须补
- 没有引用数 / venue 信息 → 必须标注
- 没区分"已被广泛接受" vs "争议中" → 必须 surface 学界共识 vs 争议
- 把 LLM 总结的"摘要"当作论文核心贡献 → 必须从原文 introduction/contribution 提炼
