# 信源分层规则（Source Tiering）

不是所有信源都同等可信。本文档定义 4 个 Tier 和打分规则，供 `scripts/source_evaluator.py` 和人工评分共用。

---

## Tier 定义

### Tier A — 一手 / 权威
- 一手数据（原始论文、SEC 财报、上市公司年报、官方统计局）
- 同行评议的学术论文（Nature / Science / 顶会、JCR Q1）
- 政府/国际组织官方发布（OECD / IMF / 世卫组织 / 中国国家统计局）
- **要求**：作者可识别、机构可验证、有出版日期

### Tier B — 二手 / 行业研究
- 知名行业研究机构（Gartner / IDC / Forrester / 麦肯锡 / 贝恩 / 艾瑞 / 头豹 / 易观 / 36 氪研究院）
- 知名财经媒体（FT / WSJ / Bloomberg / Reuters / 财新 / 经济学人）
- 知名科技媒体（The Information / Stratechery / 极客公园 / Tech 星球）
- **要求**：编辑流程可信、有作者、有发布日期

### Tier C — 一般媒体 / UGC 信号
- 一般科技/财经媒体（TechCrunch / Wired / 36 氪 / 虎嗅 / 36 氪 / 钛媒体）
- 公司官方 blog / press release（**算 Tier C 因为有 bias**，但事实陈述可以用）
- 知乎专业回答、Twitter/X 行业人士发言、播客
- 维基百科（作为 Tier B 信源的索引可以用，但不直接引用）

### Tier D — 弱信号 / 不可单独支撑
- 匿名爆料、营销稿、内容农场、SEO 文章
- 用户评论、小红书/微博 UGC（仅作为情绪/趋势信号）
- AI 生成内容（包括其他 LLM 给出的总结）
- **使用规则**：Tier D 只能作为 corroborating evidence，**禁止单独支撑结论**

---

## 自动评分规则（source_evaluator.py 的判定逻辑）

```
+3  域名匹配 Tier A whitelist
+2  域名匹配 Tier B whitelist
+1  域名匹配 Tier C whitelist
+1  作者字段存在
+1  发布日期存在且 ≤2 年
+1  HTTPS
-1  发布日期 >5 年（除非是历史/学术类 query）
-2  域名匹配已知低质 / 内容农场
-3  无作者 + 无日期 + UGC 平台
```

总分映射：
- ≥4：Tier A
- 2-3：Tier B
- 0-1：Tier C
- <0：Tier D

---

## 调用规则（Phase 4 必须遵守）

| 报告里的 claim 类型 | 最低源要求 |
|---------------------|----------|
| 关键数字（市场规模、份额、估值、增长率） | ≥3 个独立源，其中至少 1 个 Tier A 或 2 个 Tier B |
| 趋势/方向判断 | ≥2 个 Tier B 或以上 |
| 一般事实（公司成立时间、产品名）| 1 个 Tier B 或以上 |
| 引用观点（"X 公司 CEO 说..."） | 1 个 Tier B 直接引用源 |
| 推测 / 行业 sentiment | 标注为 inference，可以用 Tier C/D 信号 |

**硬约束**：报告里 Tier C 占比 >50% 直接 fail，必须补 Tier A/B 源。

---

## sources.json 数据结构

每条候选源在 `./research-vault/sources.json` 里的格式：

```json
{
  "id": "src-001",
  "url": "https://example.com/article",
  "title": "Article Title",
  "author": "Author Name or null",
  "publication": "Source Publication",
  "published_date": "2024-08-15",
  "accessed_date": "2026-05-15",
  "tier": "B",
  "tier_score": 3,
  "snippet": "first 500 chars",
  "used_in_claims": ["claim-1", "claim-3"],
  "notes": "可信度备注"
}
```

后续 critique / gap-fetch / citation 校验脚本都读这个文件。
