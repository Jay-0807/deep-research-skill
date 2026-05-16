# 场景：通用深度调研 / 混合场景 (Generic Deep Research)

## 何时触发
- 用户的 query 不明显属于上面 8 个特定场景
- 用户的 query 是多场景混合
- 用户要求"深度调研 X" 而没有明确指定角度

## 思路：用通用骨架 + 动态拼装

通用场景的核心做法：
1. **场景识别 + 拆解**：分析 query 实际隐含几个子场景
2. **动态加载相关 scenario 文件**：把命中的 scenario.md 的方法论拼起来用
3. **走完整 8 阶段流水线**（`methodology/pipeline.md`）
4. **用通用 6 段式模板**（`templates/report.md`）

---

## 三步通用方法

### Step 1：识别隐含场景

通过 query 关键词扫描，判断隐含场景：

| 信号词 | 可能场景 |
|--------|---------|
| "对比"、"vs"、"哪个好" | competitive / tech-evaluation |
| "规模"、"市场"、"增长" | market |
| "公司"、"团队"、"估值"、"融资" | due-diligence |
| "用户"、"客户"、"痛点"、"反馈" | user-research |
| "趋势"、"未来"、"前景"、"信号" | trend-foresight |
| "论文"、"文献"、"研究进展" | academic |
| "人才"、"候选人"、"薪资" | talent-research |
| 多个混合 / 都不像 | general 自己 + 拼装 |

如果识别到 2-3 个隐含场景，**逐个 Read** 对应的 scenario 文件，提取它们的 "必答问题" 合并去重，作为本次调研的子问题。

### Step 2：通用研究骨架（4 段式）

如果隐含场景识别不出，用通用的 4 段式：

1. **背景与定义**：澄清研究对象的边界 + 关键概念
2. **现状描述**：是什么 / 谁在做 / 怎么做 / 多大规模 / 多少人在用
3. **驱动 + 制约**：为什么会这样 + 什么在推进 / 阻碍
4. **判断 + 建议**：综合判断 + 给用户的 action

### Step 3：套通用 5 项检查（每次调研都跑）

- ☐ Top 3 玩家是否覆盖
- ☐ 关键数据是否 ≥3 源
- ☐ 反方 / 风险是否处理
- ☐ 中文 + 英文信源是否都有（如有相关性）
- ☐ 结论是否 actionable

---

## 推荐方法论组合

### 任何通用调研都应该有的"骨架要素"
1. **5W1H 起手**：What / Why / When / Where / Who / How 的初步答案
2. **STEEP 扫描**：社会 / 技术 / 经济 / 环境 / 政治 5 维（详见 `scenarios/trend-foresight.md`）
3. **三情景**：Bull / Base / Bear（详见 `scenarios/due-diligence.md`）
4. **冲突标注**：参考 `methodology/pipeline.md` Phase 5

---

## 推荐信源
默认全部信源管道：
- `sources/academic.md`
- `sources/industry.md`
- `sources/company.md`
- `sources/general-web.md`

按 Phase 3 检索时根据问题性质选 2-4 个最相关的。

## 推荐模板
`templates/report.md` 通用 6 段式

## 输出 deliverables
1. **Exec Summary**（≤500 字 + 3 个最关键发现 + 1 个反直觉）
2. **背景与定义**
3. **核心 findings**（按子问题）
4. **冲突与不确定性**（明确 surface）
5. **关键判断 + 建议**
6. **限制 + 未答**（必须）
7. **References**

## 反模式
- 用 general 当借口逃避场景识别 → 必须先尝试识别隐含场景
- 拼装过多 scenario 导致报告冗长 → 最多组合 3 个 scenario
- 把通用模板写得太"百科" → 必须 actionable
- 没有反方 / 限制 → 必须有
