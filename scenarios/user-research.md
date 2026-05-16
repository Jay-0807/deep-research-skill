# 场景：用户 / 客户调研 (User / Customer Research)

## 何时触发
用户问："X 用户怎么想"、"X 的用户痛点"、"X 的用户画像"、"JTBD"、"用户为什么不用 X"、"客户反馈分析"、"X 的目标用户"、"为什么 Z 世代不喜欢 X"。

> 这是生态空白点 —— 现有 skill 只有 UX Researcher 这一个名字，没有完整 SOP。本场景填补。

## 必答 6 大问题

1. **谁在用 / 不用**：Active users / Power users / Lapsed users / Non-users 各自画像
2. **JTBD（Jobs to be Done）**：用户雇佣这个产品来完成什么 "job"
3. **痛点 + 替代方案**：用户实际痛点（不是产品想解决的）+ 当前用户怎么 work around
4. **情感与态度**：对产品 / 品类 / 品牌的情感反应（爱 / 中性 / 怨 / 恨）
5. **决策路径**：从认知 → 兴趣 → 购买 → 使用 → 留存 → 推荐 每个环节的 friction
6. **洞察 + 行动建议**：3-5 个 actionable insight

## 推荐方法论

### 1. JTBD 框架（必做）
对每个目标用户群，回答 JTBD 三要素：
- **Situation**：在什么情境下出现这个需求？（when / where / triggering event）
- **Motivation**：用户真正想达成什么 outcome？（不是 feature，是 outcome）
- **Expected outcome**：成功后用户感受到什么？
- **替代方案 / Workaround**：现在用户怎么解决这个 job？（即便没有你的产品）

JTBD 写法：`When [situation], I want to [motivation], so I can [outcome].`

### 2. 痛点优先级矩阵
用两个维度排序找到关键痛点：
- 横轴：**频次**（多频繁发生）
- 纵轴：**严重度**（发生时多痛）
- 高频高严重 = 必须解决
- 高频低严重 = 持续改善
- 低频高严重 = 应急处理
- 低频低严重 = 忽略

### 3. 用户分层（4 类必分）
- **Power users**（重度用户）：留存高 / 使用深 / 推荐多
- **Active users**（普通活跃）：定期使用但无强依赖
- **Lapsed users**（流失用户）：曾用，现已不用 → **流失原因是金矿**
- **Non-users**（从未用）：知道但选了别家 / 完全不知道 → **品类层面的 gap**

对每类至少找 5-10 条 quote / case 支撑画像。

### 4. 情感扫描（Sentiment + Emotion）
不仅做正负向 sentiment，要识别具体情感：
- **沮丧 / 失望**（产品没达到预期）
- **愤怒 / 怨恨**（产品造成具体伤害：损失钱、丢面子、隐私泄露）
- **困惑 / 无助**（不会用、找不到帮助）
- **依赖 / 喜爱**（不能没有）
- **怀念 / 失落**（之前有现在没了）

不同情感对应不同 product action。

### 5. 决策路径漏斗（funnel friction map）
画出用户从认知到推荐的全链路，每个环节找：
- **流失点**：在哪里掉了多少人？
- **friction 来源**：是认知 / 信任 / 价格 / 操作 / 期待 / 替代品？
- **干预手段**：每个 friction 对应什么具体 action

### 6. 信源原则
- **永远找用户原话**，不要用研究员的总结。引用必须保留原文 + 来源 URL。
- 优先级：1v1 访谈 > 焦点小组 > 论坛长帖 > 短评论 > 客服记录 > 调研问卷 > 销售/客服自述 > 创始人臆测

## 推荐信源
- **中文 UGC**：小红书 / 微博 / 知乎 / 豆瓣小组 / B 站评论 / 抖音评论 / V2EX / 即刻
- **英文 UGC**：Reddit / Quora / Twitter/X / HackerNews / 产品类 subreddit
- **应用评价**：App Store / Google Play / 应用宝 / 小米应用商店 / G2 / Capterra / Product Hunt
- **客户支持**：公司公开的 FAQ / 客服微博 / 官方社区
- **数据洞察平台**：QuestMobile / 七麦数据 / Sensor Tower / data.ai（应用使用数据）
- **专业访谈记录**：极客公园 / 36 氪深度 / 晚点 LatePost / The Information 的用户访谈类文章

## 推荐模板
`templates/report.md` + 内嵌 JTBD 表 + 痛点矩阵 + 用户分层

## 输出 deliverables
1. **TL;DR**（一句话最关键发现）
2. **用户画像**（4 类 × 每类含人口学 + 情感 + JTBD + 代表 quote）
3. **JTBD 矩阵**（job × 用户类型 × 当前 workaround）
4. **痛点优先级矩阵**（2×2 + 具体痛点列表 + 真实 quote 支撑）
5. **决策路径 friction map**
6. **情感扫描**（情感 × 频次 + 触发场景）
7. **洞察 + 行动建议**（3-5 条，每条含：洞察 → 用户证据 → 建议 action）
8. **References**（必须保留原文 quote 的 URL）

## 反模式
- **用 LLM 编造 user persona** → 必须从真实 UGC 提取，每个画像至少 5 条 quote 支撑
- **只看正面评价** → 必须主动找 1-2 星评论 / 流失用户原因
- **把 marketing 文案当用户反馈** → 必须区分 official narrative vs user voice
- **画像是 30 岁女性白领** → 没用。必须有具体行为 / 情感 / JTBD
- **没有 JTBD 表** → 必须有
- **没有反方 / 流失原因** → 必须深挖流失用户

## 与 trend-foresight.md 的联动
用户研究里的"新兴使用场景"和"新兴吐槽"是趋势调研的高价值早期信号。如果在用户调研中发现明显的"新行为/新表达"，应建议追加 trend-foresight 调研。
