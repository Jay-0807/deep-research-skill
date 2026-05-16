# 学术信源管道

## 英文学术（优先级从高到低）

### 1. Semantic Scholar — **强推**
- URL：https://www.semanticscholar.org
- API：https://api.semanticscholar.org/graph/v1/
- 优势：免费、引用图、跨学科、有 abstract、批量查询稳定
- 限制：rate limit ~100/5min（公开 API），可申请 free API key 提升
- 用法：搜论文 / 找引用链（forward + backward）/ 抓 abstract / 看 venue + 引用数
- 何时优先：CS / AI / 跨学科都首选

### 2. arXiv
- URL：https://arxiv.org
- API：http://export.arxiv.org/api/query
- 优势：preprint 最快、ML/CS/Physics 必查
- 限制：未经同行评议、混入大量未来不会发表的工作
- 何时用：找最新论文（<3 个月）、找还在迭代的工作
- 注意：arXiv-only 论文要在报告里标注

### 3. OpenAlex
- URL：https://openalex.org
- API：https://api.openalex.org/works
- 优势：完全开放替代 Scopus、跨学科、有 institution / venue / author 元数据
- 何时用：做大范围 bibliometric 分析、找某机构的所有论文

### 4. CrossRef
- URL：https://www.crossref.org
- API：https://api.crossref.org/works
- 优势：DOI 权威解析、有 75 万种期刊数据
- 何时用：验证 DOI / 反向解析 / 获取规范引用

### 5. PubMed
- URL：https://pubmed.ncbi.nlm.nih.gov
- API：https://www.ncbi.nlm.nih.gov/books/NBK25500/
- 优势：生医文献最全
- 何时用：medical / bio / pharmacology / public health 必查

### 6. Google Scholar
- URL：https://scholar.google.com
- 优势：最全、引用计数权威
- 限制：**没有公开 API**、爬虫易被 ban、不要批量用
- 何时用：补充验证、人工查少量论文、确认引用数

### 7. NBER + SSRN
- NBER：https://www.nber.org（经济学工作论文）
- SSRN：https://www.ssrn.com（社会科学工作论文）
- 何时用：经济 / 金融 / 法律 / 社科

### 8. Papers with Code
- URL：https://paperswithcode.com
- 优势：SOTA leaderboard + 关联代码实现
- 何时用：ML 选 SOTA / 找复现代码

---

## 中文学术（优先级从高到低）

### 1. 知网（CNKI）
- URL：https://www.cnki.net
- 优势：中文期刊 / 学位论文 / 会议论文最全
- 限制：**绝大多数需要订阅或机构购买**、单篇下载付费、API 不开放
- 何时用：中文学术综述必查、但访问成本高
- 替代：先用知网搜索定位标题 + 作者，再用其他渠道找 PDF

### 2. 万方数据
- URL：https://www.wanfangdata.com.cn
- 类似知网，覆盖期刊 / 学位论文 / 会议 / 标准 / 专利
- 何时用：知网搜不到时的补充

### 3. 维普资讯
- URL：http://www.cqvip.com
- 中文期刊 + 标准
- 覆盖度略低于知网 / 万方

### 4. 国家科技图书文献中心（NSTL）
- URL：https://www.nstl.gov.cn
- 优势：政府背景、部分文献免费、覆盖中外文献
- 何时用：找不到付费源时的免费替代

### 5. 中国知网 CNKI Scholar（学术搜索）
- URL：https://scholar.cnki.net
- 类似 Google Scholar 的中文版

### 6. 百度学术
- URL：https://xueshu.baidu.com
- 优势：免费、聚合多个数据库
- 限制：质量参差，不能作为权威引用

### 7. 中国知网工程索引（EI Compendex 中文部分）
- 工科必查
- 通常需要机构访问

### 8. 中科院文献情报中心
- URL：http://www.las.cas.cn
- 学科专题报告
- 何时用：找科研政策 / 学科评估报告

---

## 学术搜索的实操建议

### 关键词扩展策略
1. 先用中英文双语搜（同一概念中英文都搜，covering 不同社区）
2. 用 synonyms 和 alternative phrasing（如 "Large Language Model" / "LLM" / "Foundation Model"）
3. 加 venue 限制（如 "NeurIPS 2024 X"）
4. 加 author 限制（找到 1 篇好论文后，搜该作者其他工作）

### 引用链溯源
- 找到 1-2 篇 seminal paper 后：
  - **Backward**：读它的 References → 找奠基论文
  - **Forward**（Semantic Scholar / Google Scholar）：→ 找后续发展
- 通常 3 跳之内覆盖 sub-topic 核心文献

### 时间窗口
- "经典 + 最新" 双跑：search 时既要 ≥5 年前的 seminal works，也要 ≤18 个月的 SOTA
- 中文学术滞后于英文 6-18 个月（在 CS / AI 领域）

### 引用质量判断
- 顶会 / 顶刊（按学科有公认列表）+ 高引用 = 必读
- 新论文（<1 年）：引用数不足以判断，看 venue + 作者背景
- 看 venue 的 acceptance rate（顶会通常 <25%）

### 反幻觉
- LLM 经常"编造看似真实"的论文名 + 作者
- **每篇引用必须用 `scripts/verify_citations.py` 验证 DOI / URL 可访问**
- 不能验证的论文不要写进报告

---

## 引用格式（统一 APA 7th）

```
Lastname, F. (Year). Title of paper. Journal Name, Volume(Issue), pages. https://doi.org/...
```

中文论文：
```
姓 名. (年份). 论文标题. 期刊名, 卷(期), 页码. URL/DOI
```

会议论文：
```
Lastname, F. (Year). Title of paper. In Proceedings of Conference Name (pp. X-Y). Publisher.
```

arXiv preprint：
```
Lastname, F. (Year). Title of paper. arXiv. https://arxiv.org/abs/XXXX.XXXXX
```
