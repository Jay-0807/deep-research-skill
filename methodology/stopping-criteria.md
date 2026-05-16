# 停止条件（Stopping Criteria）

"研究够了没"是 deep research 最难的工程问题。本文档定义双层停止条件 + Knowledge Gap 循环。

参考：OpenAI Deep Research 的双层停止 + qx-labs IterativeResearcher 的 Knowledge Gap Agent + hyperresearch 的预算约束。

---

## 双层停止条件

**任意一层满足都触发停止**。这避免单一信号导致过早或过晚停止。

### Layer 1：覆盖度停止（Coverage-based）

- ≥80% 的 Phase 2 子问题已被 findings **充分** 回答
- 没有新的 critic finding（critique 跑完一轮无 [MISSING] / [INSUFFICIENT]）
- 关键 claim 全部满足 source-tiers 的最低源要求

→ 满足即停。

### Layer 2：预算停止（Budget-based）

| Tier | 时间预算 | Web 调用上限 | 报告长度 |
|------|---------|------------|---------|
| Light | 30-45 min | 30 | 1.5-3k 字 |
| Full | 1.5-2.5h | 80 | 5-10k 字 |
| Deep | 2.5-4h | 150 | 10-20k 字 |

→ 达到 90% 预算即触发"准备收尾"，达到 100% 强制停止（即使覆盖度未达标，也要 graceful degrade 到当前手头数据）。

---

## Knowledge Gap Agent（决定要不要再跑一轮）

每完成一轮 Phase 3-5 后调用。

### Prompt 模板

```
你是 Knowledge Gap 评估官。Read 以下文件：
- ./research-vault/query.md
- ./research-vault/plan.md
- ./research-vault/findings/*.md

对 plan.md 里的每个子问题，输出：
- sub-q-id
- coverage: [充分 / 部分 / 未答]
- evidence: 引用 findings 里的具体段落证明你的判断
- next_action: [stop / search_more / reframe]
   - stop：充分回答，不需要再搜
   - search_more：列出还需要搜什么具体内容（要 specific，不是"再搜搜"）
   - reframe：子问题本身问错了，需要重新拆解

最后输出一个全局决策：
- continue_research: true/false
- reason: 一句话理由
```

### 决策规则

```
if 所有子问题都 stop AND 预算 <90%: 走完 Phase 7-8 后正常结束
elif 任何子问题 search_more AND 预算 <90%: 进入下一轮 Phase 3
elif 预算 ≥90%: 强制 stop，进入 Phase 7-8 但在报告里 acknowledge 哪些子问题未充分回答
elif 任何子问题 reframe: 回到 Phase 2 重新拆解（这种情况要 warning，因为通常意味着 Phase 1 澄清没做好）
```

---

## 反模式（禁止）

1. **跑固定步数不看 gap** — 静态预算驱动会导致简单 query 过度研究、复杂 query 浅尝辄止
2. **永远不停** — 必须服从预算硬上限
3. **静默截断** — 预算用完就强制停且不告诉用户哪些没答清楚。报告必须 surface 这些 limitations。
4. **Gap 评估时只读 plan，不读 findings** — 这样评估失真。必须 Read 实际 findings 才能判断 coverage。

---

## 输出文件

每轮 gap 评估写入 `./research-vault/gap-log.md`：

```markdown
## Round 1 (2026-05-15 14:23)
- 预算消耗：18 / 80 web 调用
- 子问题覆盖：
  - sub-q-1: 充分 (3 个 Tier B 源)
  - sub-q-2: 部分（缺定价对比）→ search_more
  - sub-q-3: 未答 → search_more
- 决策：continue_research = true
- 下一轮目标：补 sub-q-2 的定价 + sub-q-3 的全部

## Round 2 (2026-05-15 14:58)
...
```

这份 log 在最终交付时作为"研究透明度"附件给用户看。
