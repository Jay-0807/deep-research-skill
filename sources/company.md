# 公司信息信源管道

调研某家公司时（尽调 / 竞品 / 团队画像）必查的信源。

---

## 中国公司

### 工商 / 注册信息（一手）
- **国家企业信用信息公示系统** — http://www.gsxt.gov.cn — **官方权威，免费**
  - 必查项：注册资本、股东、变更记录、年报、行政处罚、经营异常名录
- **企查查** — https://www.qcc.com — 商业聚合，UI 友好（付费会员）
- **天眼查** — https://www.tianyancha.com — 同类，部分功能免费
- **启信宝** — https://www.qixin.com — 同类，部分版本更细
- **使用建议**：先用国家系统查权威信息，企查查 / 天眼查 用于历史变更 / 关联企业图谱（这部分官方不直观）

### 信用 / 处罚
- **信用中国** — https://www.creditchina.gov.cn — 行政处罚、失信被执行人
- **裁判文书网** — https://wenshu.court.gov.cn — 司法判决（注意：近年公开度收紧）
- **执行信息公开网** — http://zxgk.court.gov.cn

### 上市公司
- **巨潮资讯** — http://www.cninfo.com.cn — A 股 + 港股 + 北交所全披露
- **港交所披露易** — https://www.hkexnews.hk
- **SEC EDGAR**（中概股）— https://www.sec.gov/edgar.shtml
- **必查文件**：招股书 / 年报 (10-K / 20-F) / 季报 / 重大事项

### 创投 / 融资
- **IT 桔子** — https://www.itjuzi.com — 中国创投数据最全
- **36 氪 Tracker / Pro 创投** — https://36kr.com
- **投中网** — https://www.chinaventure.com.cn
- **烯牛数据** — https://www.xiniudata.com
- **鲸准 / 鲸跃** — https://rong.36kr.com

### 团队 / 招聘信号
- **拉勾** / **Boss 直聘** / **猎聘**：当前在招岗位 → 推断公司在押注什么方向
- **LinkedIn 中国**：员工背景 / 流动
- **脉脉**：员工评价 / 公司动态 / 行业 KOL 发言
- **看准网**：员工评分 / 面试经历

### 媒体报道
- 参考 `sources/industry.md` 中文 Tier A/B 媒体
- 重点：财新 / 晚点 / 36 氪深度 / 极客公园 的深度专访

### 关联信息
- **CNIPA 专利**（国家知识产权局）— http://pss-system.cnipa.gov.cn — 专利申请 / 授权
- **商标局** — https://sbj.cnipa.gov.cn — 商标
- **域名 whois**：whois.aliyun.com 等 — 公司互联网资产侧写
- **ICP 备案** — https://beian.miit.gov.cn

---

## 海外公司

### 工商注册
- **OpenCorporates** — https://opencorporates.com — 全球公司数据
- **Companies House**（UK）— https://www.gov.uk/government/organisations/companies-house
- **EDGAR**（US SEC）— https://www.sec.gov/edgar.shtml — US 上市公司必查
  - 必读：10-K（年报）/ 10-Q（季报）/ 8-K（重大事项）/ S-1（招股书）/ DEF 14A（股东大会）
- **欧盟成员国各自的 corporate registry**（按国家查）

### 投融资数据
- **Crunchbase** — https://www.crunchbase.com — 全球创投数据
- **PitchBook** — https://pitchbook.com — VC / PE / 估值（付费）
- **CB Insights** — https://www.cbinsights.com（付费）
- **Tracxn** — https://tracxn.com — 全球创新公司数据
- **Dealroom** — https://dealroom.co — 欧洲创投
- **AngelList** — https://wellfound.com — 早期创业 + 招聘

### 团队 / 人员
- **LinkedIn** — https://www.linkedin.com — 标配
- **The Org** — https://theorg.com — 公司组织架构图
- **Crunchbase Person profiles** — 个人融资 / 创业历史

### 员工评价
- **Glassdoor** — https://www.glassdoor.com — 员工评分 + 面试 + 薪资
- **Blind** — https://www.teamblind.com — 匿名职场社区（信号强但偏负面）
- **Comparably** — https://www.comparably.com — 员工 / 文化评分
- **Levels.fyi** — https://www.levels.fyi — 薪资 + level 数据（科技公司）

### 媒体报道
- 参考 `sources/industry.md` 英文 Tier A/B 媒体
- 重点：FT / WSJ / Bloomberg / The Information / Stratechery 的公司专文

### 信用 / 法律
- **PACER**（US 法庭文件）— https://pacer.uscourts.gov
- **Justia** — https://www.justia.com — US 案例搜索
- **D&B Hoovers**（付费）— 全球企业信用 / 财务

### 产品 / 技术信号
- **GitHub** — https://github.com — 工程团队的代码 / 活跃度
- **Built With** — https://builtwith.com — 网站技术栈
- **SimilarWeb** — https://www.similarweb.com — 网站流量
- **Apptopia / data.ai** — App 数据
- **Patents**：Google Patents — https://patents.google.com

---

## 调研某公司的标准查询清单

调研任何公司必跑的 10 项检查（中国版）：

```
☐ 1. 国家企业信用公示系统：注册资本、股东、变更
☐ 2. 企查查 / 天眼查：关联企业图谱、历史融资
☐ 3. IT 桔子 / 36 氪：详细融资历史 + 估值
☐ 4. 信用中国 + 裁判文书网：处罚 / 诉讼
☐ 5. LinkedIn / 脉脉：核心团队 + 流动
☐ 6. 看准网 / 脉脉：员工评价
☐ 7. 拉勾 / Boss 直聘：当前招聘需求 → 业务方向信号
☐ 8. CNIPA：专利申请 / 授权数 + 技术方向
☐ 9. 财新 / 晚点 / 36 氪深度：深度报道
☐ 10. 微博 / 知乎：创始人 / 高管个人形象 + 争议
```

海外公司 10 项：

```
☐ 1. EDGAR / 当地 corporate registry：注册 + 财务（如上市）
☐ 2. Crunchbase + PitchBook：融资 + 估值
☐ 3. OpenCorporates：实体结构
☐ 4. PACER + Justia：诉讼
☐ 5. LinkedIn + The Org：团队
☐ 6. Glassdoor + Blind：员工评价
☐ 7. Levels.fyi：薪资水平
☐ 8. Google Patents：专利
☐ 9. FT / WSJ / Bloomberg / The Information：深度报道
☐ 10. Twitter / Reddit：创始人 / 公司舆论
```

---

## 反幻觉警示

调研公司时 LLM 最容易编：
- ❌ 编造的融资轮次 / 金额（必须从 Crunchbase / IT 桔子 等具名源验证）
- ❌ 编造的创始人履历（必须 LinkedIn / 媒体专访交叉验证）
- ❌ 编造的客户名单（marketing 页面的客户 logo 也可能是 paid pilot 而非真实大客户）
- ❌ 编造的产品价格（必须查实际定价页或销售文档）

**调研公司时所有具体数字都必须有可点击的源 URL**，否则改写为"约 / 据传 / 公开未披露"。
