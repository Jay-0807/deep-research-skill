# 通用调研流水线（8 阶段）

这是所有 scenario 共用的研究骨架。任何一次调研都按这 8 阶段走，**Phase 1/2/3/4/7 不可省**，5/6/8 在 light tier 调研里可酌情简化。

骨架来源：`hyperresearch` 16 步精简版 + `199-bio` 的 8-phase + `gpt-researcher` 的 7 步线性流的混合。

---

## Phase 1：澄清（Clarification）

**目标**：把用户模糊的需求转成 canonical query 文件，避免下游 subagent 各自理解不一。

**动作**：
1. 主动反问 **最多 3 个** 关键问题（不要问没用的），例如：
   - 研究范围（地区/时间窗/目标读者）
   - 深度（light/full tier）
   - 关键约束（不能用某些信源、必须包含某些维度）
2. 用户回应后，把"用户原 prompt + 你的澄清问题 + 用户回应"合成一份 **canonical query**，写入 `./research-vault/query.md`。
3. 所有 subagent 在自己的步骤里都**必须先 Read query.md**，不允许凭记忆操作（防 LLM 漂移）。

**完成标志**：`query.md` 存在，包含"任务陈述 / 范围 / 时间窗 / 目标读者 / 深度等级 / 关键约束"6 项。

---

## Phase 2：拆解（Decomposition）

**目标**：把 canonical query 拆成 5-15 个可独立检索的子问题。

**两种拆解策略，按场景选**：

### 策略 A：STORM Perspective Discovery（推荐用于学术/竞品/市场）
1. 先用 WebSearch 找 **1-3 篇已有的优秀同类报告**（例如调研 AI Agent 创业公司前，先搜 a16z、Sequoia、艾瑞的 AI Agent 报告）
2. 提取这些报告用过的 **outline 视角**（例如：市场规模 / 玩家分布 / 商业模式 / 技术路线 / 监管 / 资本动向）
3. 用这些视角作为你的子问题骨架

### 策略 B：Anthropic 四件套委派（推荐用于尽调、用户研究、技术选型）
对每个子问题，明确写出 4 个字段（参考 `methodology/source-tiers.md` 里的 task spec template）：
- **objective**（这个子问题要回答什么）
- **output format**（要什么形式的结果：表格 / 列表 / 数字 / 文字）
- **tool guidance**（推荐用哪些信源）
- **clear boundaries**（什么不要做：不要算总和、不要给意见、只列事实）

**完成标志**：`./research-vault/plan.md` 列出所有子问题 + outline，每个子问题包含上述 4 字段。

**反模式（禁止）**：
- 子问题数量 <3（拆得太粗）或 >20（拆得太碎）
- 子问题之间高度重叠
- 出现"研究 X 的所有情况"这种开放问题

---

## Phase 3：检索（Retrieval）

**目标**：对每个子问题做多源并行检索，建立 candidate sources 池。

**动作**：
1. 对每个子问题，根据 scenario 推荐的 `sources/*.md` 选 **2-4 个互补信源**（不是越多越好）
2. 并行 WebSearch / WebFetch（如果有 MCP 工具则用之）
3. 学术问题：优先 Semantic Scholar API / arXiv API，不要直接 Google
4. 中文问题：必须包含中文信源管道（参考 `sources/industry.md` 中文部分）
5. 把所有检索到的 URL/标题/snippet 写入 `./research-vault/sources.json`（结构在 `methodology/source-tiers.md`）

**预算约束**（防止失控）：
- light tier：每个子问题 ≤5 次 web 调用，总计 ≤30 次
- full tier：每个子问题 ≤15 次，总计 ≤80 次
- 单次响应超过 50KB 必须摘要后再继续

**完成标志**：`sources.json` 至少包含 10 条（light）或 30 条（full）候选源。

---

## Phase 4：提取 + 可信度评分（Extraction & Source Tiering）

**目标**：从候选源里筛出可用的，给每条事实打源标记。

**动作**：
1. 对每条候选源跑 `scripts/source_evaluator.py`（或在内联 prompt 里按 `methodology/source-tiers.md` 的分层规则人工评分）
2. 一手 / 同行评议 / 官方统计 → **Tier A**
3. 行业研究机构（Gartner/IDC/艾瑞）/ 知名媒体（路透/Bloomberg/财新）→ **Tier B**
4. 一般媒体 / 博客 / UGC → **Tier C**
5. 匿名 / 营销稿 / 无作者 → **Tier D**（仅作信号，不能单独支撑结论）
6. 对每个子问题，从源里提取关键事实，写入 `./research-vault/findings/sub-qN.md`，每条事实带 **(Tier, URL, 提取日期)** 三元组

**完成标志**：每个子问题对应一份 findings.md，每条事实可追溯到具体 URL。

---

## Phase 5：冲突标注（Conflict Surfacing）

**目标**：把不同源之间的矛盾**显式 surface 出来**，不让 LLM 静默融合。

**动作**：
1. 扫所有 findings/*.md，找事实级冲突（同一指标不同数据、同一事件不同表述）
2. 对每个冲突，写入 `./research-vault/conflicts.md`，格式：
   ```
   ### 冲突 N：关于 X 的数据
   - 源 A（Tier B, 2024-08）：X = 1000
   - 源 B（Tier A, 2024-12）：X = 1500
   - 可能原因：统计口径差异 / 时间不同 / 估算 vs 实测
   - 我的判断：采用源 B，因为 Tier 更高且时间更近
   ```
3. **重要冲突在最终报告里也必须显式提及**，不允许偷偷选一个版本。

**完成标志**：conflicts.md 存在（即便没找到冲突，也写 "no significant conflicts found"，证明你确实扫了）。

> 这是生态空白点之一。多数 deep research 工具都把冲突信息静默融合，本 skill 强制 surface。

---

## Phase 6：Knowledge Gap 循环（动态停止）

**目标**：判断"研究够了没"。不靠静态预算，靠 gap analysis。

**动作**（每完成一轮 Phase 3-5 后执行）：
1. Read `plan.md` 里的所有子问题
2. 对每个子问题打分：是否已被 findings 充分回答？（充分 / 部分 / 未答）
3. 找出 **"部分"** 或 **"未答"** 的子问题 → 决定是否再跑一轮 Phase 3
4. 双层停止条件（hyperresearch + OpenAI Deep Research 思路）：
   - **覆盖度信号**：所有子问题 ≥80% 被充分回答 ✅
   - **预算信号**：已用 web 调用 ≥ budget × 90% ⚠️
   - **任何一个满足都触发停止**

**完成标志**：写入 `./research-vault/gap-decision.md`，记录每轮的 gap 判断和决策。

**反模式**：
- 静态走完固定步数不看 gap
- gap 永远不满足、无限循环（必须服从预算硬上限）

---

## Phase 7：综合写作（Synthesis）

**目标**：把所有 findings 综合成最终报告。

**关键原则**：**outline-first + patch-never-regenerate**

**动作**：
1. **先生成 outline**（写入 `./research-vault/report-outline.md`），不写正文
2. 对每个 section 单独生成正文（section-by-section），先写"骨"再写"肉"
3. 选择 `templates/*.md` 里合适的模板套
4. 一次生成完整草稿后，**后续所有修改必须是 surgical edit（Edit 而非 Write）**，禁止整段重写。这是 hyperresearch 的"patch, never regenerate"原则——防 LLM 把前面累积的事实丢掉。
5. 每段都必须有内联引用 `([source title](url))`，末尾附 References 段
6. 引用规范直接抄 gpt-researcher 的 APA 格式（参考 `templates/report.md`）

**完成标志**：`./research-vault/report.md` 存在，所有 claim 有源，符合模板结构。

---

## Phase 8：对抗式 Critique（Adversarial Review）

**目标**：用 4 个不同角度的 critic 来挑报告毛病，然后 patch。

**4 个 Critic 角度**（参考 hyperresearch）：
1. **Dialectic Critic**：反方观点是否被认真对待？有没有 strawman？
2. **Depth Critic**：哪些 claim 只有 1-2 个源？是否需要补 3-5 个？哪些 Tier C/D 源支撑了关键结论？
3. **Width Critic**：是否覆盖了所有 Phase 2 拆解的子问题？有没有遗漏明显的相关角度？
4. **Instruction Critic**：是否完整回答了用户原 prompt？是否漂移到了无关话题？

**动作**：
1. 启动 4 个 Read-only 的 sub-thinking pass（或 4 次内部 self-review）
2. 把每个 critic 的发现写入 `./research-vault/critique.md`
3. 对每条 critique，决定：**patch（surgical edit）** / **gap-fetch（回到 Phase 3 补一次检索）** / **acknowledge（在报告里加 limitations 段说明）**
4. **Patch 动作的工具必须锁定在 Read+Edit，不允许 Write**（防 LLM 把好不容易写完的报告整段重写）

**完成标志**：critique.md + 所有 patch 已应用 + report.md 已更新

---

## Phase 9（强制后置）：脚本校验

跑：
```bash
python scripts/verify_citations.py ./research-vault/report.md
python scripts/validate_report.py ./research-vault/report.md
```

任一脚本报错 → 修复 → 重跑。全绿才能向用户呈现。

---

## Tier 选择指南

| 用户场景 | 推荐 Tier | 预算 |
|---------|----------|------|
| 用户说"快速看看 X" | **Light** | ~10 源 / 30 min / 跳过 Phase 5、简化 6、跳过 8 |
| 用户说"调研" / "研究" | **Full** | ~30 源 / 1.5h / 全 9 阶段 |
| 用户说"深度调研" / "完整报告" / "投资决策依据" | **Deep** | ~60 源 / 2.5h / 全 9 阶段 + 每个 critic 都跑 + 重要 claim ≥5 源 |

不要默认 Full，让用户在 Phase 1 澄清时选。
