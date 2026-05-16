# 场景：市场 / 行业调研 (Market & Industry Research)

## 何时触发
用户问："X 市场多大"、"X 行业研究"、"X 的市场规模 / 增长 / 趋势"、"X 行业的价值链"、"X 的监管环境"、"X 的客户细分"。

## 必答 7 大问题

1. **市场规模**：TAM / SAM / SOM 三层
2. **增长率**：历史 CAGR + 未来 5 年预测 + 关键驱动因素
3. **价值链**：上游 / 中游 / 下游 + 利润池分布
4. **客户细分**：人口 / 心理 / 行为 / 地理 / 价值 / 生命周期 7 维
5. **监管 / 政策环境**：现有监管 + 政策风向 + 合规成本
6. **关键趋势**：3-5 个塑造市场的趋势 + 信号源
7. **风险与机会**：5 个最值得关注的

## 推荐方法论

### 1. Top-down + Bottom-up 双重验证（来自 pytrak89/market-research）
- **Top-down**：从行业报告（Gartner / IDC / 艾瑞）拿大数。**永远不要只信一家**，至少 3 家交叉验证。
- **Bottom-up**：用真实获客单价 × 潜在客户数 自下而上算一遍。
- **两个数差异 >30% 说明 top-down 数据有问题**，要在报告里 surface 这个差异。

### 2. 价值链拆解（Porter 五力的简化版）
对每个环节回答：
- 主要玩家 + 集中度（CR3、CR5）
- 利润率 + 议价能力
- 进入壁垒
- 替代品威胁

### 3. 客户细分的 7 维（来自 VoltAgent/market-researcher）
不要只用 demographic。完整 7 维：
- Demographic（年龄/性别/收入/教育）
- Psychographic（价值观/生活方式/兴趣）
- Behavioral（使用频率/品牌忠诚/购买决策路径）
- Geographic（地区/城市级别/气候）
- Value-based（客单价/LTV/利润贡献）
- Life-cycle（新客/活跃/沉默/流失）
- Need-based / JTBD（雇用产品来做什么 job）

不需要 7 维全做，但选 3-4 维必须有理由。

### 4. 监管 / 政策维度（中文场景必做）
- 中国市场必查：国家发改委 / 工信部 / 国务院发文、十四五/十五五规划、地方政府试点
- 必须区分"已落地法规" vs "讨论中的政策风向"
- 政策对市场的具体影响要量化（影响多少 GMV / 减少多少玩家 / 推迟多少时间）

### 5. 趋势识别（与 trend-foresight.md 联动）
3-5 个塑造市场的趋势，每个必须包含：
- 信号源（≥3 个独立信号）
- 时间窗（已发生 / 1-3 年 / 3-5 年）
- 影响判断（颠覆性 / 加速性 / 调整性）

## 推荐信源
- 主要：`sources/industry.md`（行业报告机构）+ `sources/company.md`（玩家信息）
- 学术补充：`sources/academic.md`（特别是 Top-down 数据找原始研究）
- 中文必加：艾瑞 / 头豹 / 易观 / 36 氪研究院 / 亿欧智库 / IT 桔子
- 英文必加：Statista / IBISWorld / Gartner / IDC / Forrester / McKinsey

## 推荐模板
`templates/report.md` 通用 6 段式

## 输出 deliverables
1. **Exec Summary**（≤500 字，必须包含 3 个最关键数字 + 1 个最反直觉的发现）
2. **Market Sizing**（TAM/SAM/SOM 表 + 增长率 + 驱动因素）
3. **Value Chain**（按环节）
4. **Customer Segments**（≥3 维细分 + 主要客群画像）
5. **Trends**（3-5 个）
6. **Regulatory**（监管 + 政策风向）
7. **Risks & Opportunities**（各 5 个）
8. **Recommendation**（针对用户的具体决策）
9. **References**

## 反模式
- 直接抄一家报告的数 → 必须交叉验证
- 只有 top-down，没有 bottom-up sanity check → 强制补
- 政策段写得很泛（"政府支持 / 政策利好"）→ 必须给具体文件名、发文时间、量化影响
- 把市场报告写成"行业百科" → 必须有可执行 recommendation
