# 对抗式 Critique 循环

报告草稿完成后的"找茬"流程。借鉴 hyperresearch 的 4 个 adversarial critic + 199-bio 的 critique loop-back。

---

## 为什么要做 critique

LLM 自评有强烈的"过度自信偏差"——同一个模型写完报告后说"质量很好"。Critique 用 **对抗式角色扮演** 强迫模型从不同角度找毛病。

经验上 critique 能发现 30-50% 的：
- 没有反方观点的单边论述
- Tier C/D 源支撑了关键 claim
- 关键子问题被遗漏
- 报告偏离了用户原 prompt

---

## 4 个 Critic（角色扮演 prompt）

### Critic 1：Dialectic Critic（反方代理人）

```
你是一名严格的同行评议者，正在审查一份调研报告。你的任务：
1. 找出报告里所有"明显倾向某一方"的判断
2. 对每个倾向判断，写出 ≥1 个具体的反方论据（可以是数据、案例、观点）
3. 检查报告是否处理了这些反方论据：
   - 处理了 → 标记 [OK]
   - 提到但没认真讨论 → 标记 [STRAWMAN]
   - 完全没提 → 标记 [MISSING]
4. 任何 [STRAWMAN] / [MISSING] 都必须 patch
```

### Critic 2：Depth Critic（深度审查）

```
你是一名 fact-checker。逐条扫描报告里的所有 claim（数字、断言、引用）：
1. 对每条 claim，count 它有几个独立源（不算同一原文的多次引用）
2. 标记：
   - 关键数字源 <3 → [INSUFFICIENT_KEY]
   - 趋势判断源 <2 → [INSUFFICIENT_TREND]
   - 主要 claim 由 Tier C 源单独支撑 → [WEAK_SOURCE]
3. 任何 [INSUFFICIENT_*] / [WEAK_SOURCE] 都触发 gap-fetch
```

### Critic 3：Width Critic（宽度审查）

```
Read ./research-vault/plan.md（Phase 2 拆解的子问题列表）。
Read 最终 report.md。
1. 对每个子问题，判断报告里是否充分回答：
   - 充分（专门一段或一节）→ [OK]
   - 部分（提到但没展开）→ [PARTIAL]
   - 未答（完全缺失）→ [MISSING]
2. 同时检查是否有"明显应该有但 plan 里没拆出来"的角度：
   - 例如调研竞品报告里没提监管 / 没提客户案例 / 没提团队
3. 任何 [PARTIAL] / [MISSING] / 缺失角度 都触发 gap-fetch
```

### Critic 4：Instruction Critic（任务符合度）

```
Read ./research-vault/query.md（canonical query）。
Read 最终 report.md。
1. 用户原 prompt 提到的所有 "deliverable" 是否都在报告里？
   （如：用户说"给我一个对比表 + 推荐"，是否两个都有）
2. 报告的 tone / 长度 / 目标读者 是否符合 query 里的要求？
3. 报告是否漂移到了用户没要的话题？
4. 任何不符 → 直接 patch
```

---

## Critique 执行流程

```
Phase 7 完成（report.md 草稿）
  ↓
启动 4 个 critic（并行或串行，并行更快）
  ↓
每个 critic 输出到 ./research-vault/critique-{1-4}.md
  ↓
合并所有 finding 到 ./research-vault/critique-summary.md
  ↓
对每条 finding 分类决策：
  - [patch]      → 用 Edit（不是 Write！）改 report.md
  - [gap-fetch]  → 回 Phase 3 做一次定向检索，再回 Phase 7 用 Edit 加入
  - [accept]     → 在 report.md 末尾的 "Limitations" 段说明该缺陷
  ↓
所有 finding 都被处理后，Critique 阶段结束
  ↓
进入 Phase 9（脚本校验）
```

---

## 工具锁定（重要）

Critic 和 Patcher 的工具权限要**显式锁定**，防 LLM 把报告整段重写丢掉前面的事实：

| Agent | 允许的工具 | 禁止的工具 |
|-------|----------|----------|
| Critic（任何 1-4 号） | Read | Write、Edit |
| Patcher（执行修改） | Read、Edit | Write |
| Gap-fetcher | Read、WebSearch、WebFetch、Write（只写 findings/） | Edit report.md（必须经 patcher） |

这是 hyperresearch 的 "patch, never regenerate" 原则的强约束实现。

---

## Light tier 的简化版

如果用户选了 Light tier：只跑 **Critic 4（Instruction）** + **Critic 2 选做** 中的关键数字检查。其余 critic 跳过。

Full / Deep tier 必须跑全部 4 个 critic。

---

## Critique 的退出条件

- 全部 critic 跑完一轮
- 所有 finding 已被处理（patch / gap-fetch / accept）
- 没有新的 [MISSING] / [INSUFFICIENT] 标记

**禁止无限循环**。如果跑了 2 轮 critic 还有 finding，说明研究本身有结构性缺陷，必须把这些缺陷写进 report.md 的 Limitations 段交付，不要继续刷。
