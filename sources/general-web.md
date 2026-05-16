# 通用 Web 搜索信源

底层 web 搜索能力。这些是基础工具，几乎所有 scenario 都会用。

---

## 搜索引擎（多源对照）

### 1. Google — 默认
- **优势**：覆盖最全、排序算法最强
- **劣势**：中文内容覆盖不如百度 / 搜狗、被广告污染
- **适用**：英文搜索、技术文档、学术、海外信息
- **使用建议**：用 advanced syntax — `site:` / `filetype:pdf` / `intitle:` / `inurl:` / `"exact phrase"`

### 2. Bing
- **优势**：API 友好（Bing Search API）、中文覆盖好于 Google、能搜中国大陆部分内容
- **适用**：中英混合查询、需要 API 调用时

### 3. Brave Search
- **优势**：注重隐私、独立索引、不被 SEO 重度污染
- **API**：https://api.search.brave.com — 商用付费
- **适用**：希望避开 Google 主导算法的偏见时

### 4. DuckDuckGo
- **优势**：隐私、可匿名
- **劣势**：索引覆盖不如 Google
- **适用**：补充查询

### 5. 百度 / 搜狗 / 360 搜索（中文）
- **百度**：中文内容最全，但商业广告 / 百家号污染严重
- **搜狗**：微信公众号专搜（http://weixin.sogou.com）— 中文行业洞察必备
- **360 / 必应中国**：补充

### 6. Yandex
- 俄文 / 东欧覆盖
- 有时能找到 Google 找不到的内容

---

## AI / Agent 优化的搜索 API

### 1. Tavily
- URL：https://tavily.com
- 专为 LLM agent 设计，返回 LLM-friendly 的搜索结果
- 有免费 tier
- gpt-researcher 默认搜索引擎

### 2. Serper
- URL：https://serper.dev
- Google 搜索的 LLM API 封装
- 速度快、便宜
- 返回原始 Google SERP

### 3. Exa（原 Metaphor）
- URL：https://exa.ai
- 语义搜索、特别适合找"类似的内容"
- 适合做引文链溯源

### 4. Jina Reader / Jina Search
- URL：https://jina.ai
- 把任意 URL 转成 LLM-friendly markdown
- `https://r.jina.ai/<URL>` 直接获取

### 5. Firecrawl
- URL：https://www.firecrawl.dev
- 网页爬取 + 结构化
- 适合批量抓站

### 6. SearchAPI
- URL：https://www.searchapi.io
- 多搜索引擎统一 API（Google / Bing / YouTube / News）

### 7. Perplexity API
- URL：https://docs.perplexity.ai
- 搜索 + LLM 综合（Online models）
- 适合一站式 search + summarize

---

## 专门类搜索

### 新闻
- **Google News** — https://news.google.com
- **News API** — https://newsapi.org
- **百度新闻** — https://news.baidu.com
- **新浪新闻** / **凤凰新闻**

### 视频内容
- **YouTube**（含 transcript 提取）
- **B 站**（中文视频）
- **抖音 / 快手**（短视频信号）
- 工具：yt-dlp（下载）、whisper / Funasr（转录）

### 播客 / 音频
- **Apple Podcasts** / **Spotify Podcasts** — 海外播客
- **小宇宙** — https://www.xiaoyuzhoufm.com — 中文播客最大平台
- **Substack Audio** — 中产化播客
- 工具：可下载音频后 transcribe

### 论坛 / UGC
- **Reddit** — 主题分类查找最强、`old.reddit.com` 用 search 限制 subreddit
- **HackerNews** — Tech 深度讨论 + 评论质量高
- **Quora** — 问答（质量参差，但偶有深度回答）
- **知乎** — 中文深度问答
- **V2EX** — 中文程序员社区
- **即刻** — 中文短帖（KOL 早期信号）
- **小红书** — 中文消费 / 生活方式 / 种草
- **微博** — 中文热点
- **豆瓣小组** — 中文亚文化 / 兴趣社群

### 文档 / PDF
- 用 `filetype:pdf` 搜索 + `site:` 限制
- 学术 PDF：参考 `sources/academic.md`
- 行业报告 PDF：参考 `sources/industry.md`
- 政府报告 PDF：直接搜部委官网

### 维基 / 知识库
- **Wikipedia 英文 / 中文** — 作为索引可以用，但不直接引用
- **Wikidata** — 结构化数据
- **Stack Overflow** — 编程问题
- **百度百科** / **互动百科** — 中文百科（注意质量差异）

---

## 高级搜索语法（必会）

### Google / Bing 通用
```
"exact phrase"           # 精确匹配
site:example.com         # 限定站点
-site:example.com        # 排除站点
filetype:pdf             # 文件类型
intitle:keyword          # 标题包含
inurl:keyword            # URL 包含
before:2024-01-01        # 日期范围 (Google)
after:2024-01-01
related:example.com      # 相似站点
"X OR Y"                 # 或
```

### 实操组合
```
# 找某主题最新行业报告
"X market size" filetype:pdf after:2024-06-01

# 找某公司用户的真实抱怨
"公司名" 评价 -官方 -招聘 site:zhihu.com

# 找某领域顶会论文
site:openreview.net "X" 2024

# 找某公司的关键事件
"公司名" (融资 OR 收购 OR 离职 OR 诉讼) site:36kr.com
```

---

## 翻墙 / 跨地区访问

调研有时需要查在墙内 / 墙外的不同信源：
- 中国大陆用户访问 Google / FT / Bloomberg / Twitter / Reddit：需要 VPN
- 海外用户访问百度 / 知乎 / 微博 / 抖音：部分内容会要求登录
- 不同地区的 Google 结果不同（如 .com vs .com.hk vs .jp），可以多地查询
- 善用 archive.org 找已删除 / 已变更的页面

---

## 反幻觉 + 信源验证

LLM 用 web search 结果时常见错误：
1. **结果幻觉**：编造看似真实的 URL（必须真访问 + 解析）
2. **过期信息**：搜索结果常包含旧内容（必须看 publication date）
3. **混淆同名实体**：同名公司 / 人 / 产品，必须 verify identifier
4. **断章取义**：摘录 snippet 时丢失上下文

**规则**：
- 任何 web 检索结果必须 WebFetch 实际 URL 二次验证
- 摘录 quote 必须保留原始 URL 在最终 citation 里
- 任何"日期相关"的数据必须看 publication date

---

## 何时优先选哪个

| 用途 | 优先 |
|------|------|
| 第一轮宽泛探索 | Google / Bing |
| 找类似内容 | Exa |
| LLM 自动化检索 | Tavily / Serper / Jina |
| 提取 URL 内容到 markdown | Jina Reader / Firecrawl |
| 微信公众号内容 | 搜狗微信 |
| 视频 / 播客 transcript | yt-dlp + Whisper |
| 中文 UGC | 百度 + 知乎 + 微博 + 小红书 |
| 已删除 / 历史版本 | archive.org / web.archive.org |
| 学术 | 参考 `sources/academic.md` |
| 行业报告 | 参考 `sources/industry.md` |
| 公司信息 | 参考 `sources/company.md` |
