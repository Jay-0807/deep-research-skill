# 学术综述报告模板

适用：`scenarios/academic.md`

风格：综合 STORM Wikipedia-style + 传统 literature review

---

## 模板

```markdown
# {主题} 文献综述

> **领域**：{e.g. NLP / Computer Vision / Theory}
> **时间范围**：{e.g. 2020-2025 / 全部历史}
> **综述范围**：{covered / excluded}
> **撰写日期**：{YYYY-MM-DD}
> **总论文数**：{N}（顶会 {x} / 顶刊 {y} / arXiv-only {z}）

---

## 1. Introduction

### 1.1 领域定义
{这个领域研究什么？关键概念定义}

### 1.2 重要性
{为什么这个领域重要？应用场景？}

### 1.3 综述范围
{覆盖哪些子方向 / 排除哪些 / 时间窗 / 语言}

---

## 2. Background & Foundations

### 2.1 历史脉络
{领域的关键里程碑事件，按时间线}

- **{Year}**：{milestone 1，含奠基论文引用}
- **{Year}**：{milestone 2}
- ...

### 2.2 奠基论文 (Seminal Papers)

| 论文 | 年份 | 核心贡献 | 引用数 |
|------|------|---------|------|
| [Title 1](url) | 2017 | 提出 X 框架 | 12000+ |
| [Title 2](url) | 2019 | 首次实现 Y | 5000+ |
| ... | | | |

### 2.3 关键概念 / 术语
{定义 5-10 个核心概念}

---

## 3. Taxonomy of Approaches

{这个领域的研究分类。可按：方法 / 任务 / 应用 / 范式 等维度分。}

```
{主题}
├── 方法范式 1（如 Transformer-based）
│   ├── 子类 1.1
│   ├── 子类 1.2
│   └── 子类 1.3
├── 方法范式 2（如 Diffusion-based）
│   ├── ...
└── 方法范式 3
    └── ...
```

**Taxonomy 来源**：{基于哪一两篇 survey 的分类，或我自己的综合}

---

## 4. State of the Art

按 Section 3 的 taxonomy，每个分支介绍 SOTA。

### 4.1 {方法范式 1}

#### 4.1.1 核心思路
{这个范式的关键 idea}

#### 4.1.2 代表工作（按时间顺序）

- **{Paper A}** (Venue Year, [link](url))
  - **关键贡献**：{contribution}
  - **方法 (TL;DR)**：{1-2 句}
  - **结果**：{benchmark on dataset = X% / Y SOTA}
  - **影响**：{后续工作如何 build on it}
  - **局限**：{已知 limitation}

- **{Paper B}** (Venue Year, [link](url))
  - ...

#### 4.1.3 该范式的优势 / 局限

### 4.2 {方法范式 2}
...

---

## 5. Benchmark / Dataset 现状

### 5.1 常用 Benchmark
| Benchmark | 任务 | 主要指标 | 当前 SOTA | 引用 |
|----------|------|---------|----------|------|
| {name} | {task} | {metric} | {model + score} | [link](url) |

### 5.2 数据集
{主流 dataset + 限制 + 偏见问题}

### 5.3 评测方法 / 争议
{评测方法本身的问题，如：benchmark contamination / dataset bias}

---

## 6. Methods Comparison

横向对比表：

| 方法 | 提出年 | 数据效率 | 计算成本 | 准确性 (X benchmark) | 可扩展性 | 主要缺陷 |
|------|-------|---------|---------|------------------|---------|---------|
| A | 2020 | 中 | 高 | 85.3 | 强 | 大模型才有效 |
| B | 2022 | 高 | 中 | 88.1 | 中 | 需特殊数据 |
| C | 2024 | 低 | 低 | 84.7 | 弱 | 仅限单语言 |

---

## 7. Open Problems & Future Directions

### 7.1 公认未解决问题
{领域内 survey / 重要会议 keynote 反复提及的开放问题}

1. **{Open problem 1}**：{描述} — 已有尝试 [refs]，但尚未解决因 {reason}
2. **{Open problem 2}**：
3. ...

### 7.2 新兴方向
{近 1-2 年开始出现、但尚未成主流的方向}

### 7.3 争议
{学界内部尚有争议的话题，列出双方观点}

- **争议 1**：{topic}
  - 立场 A：{argument + supporters [refs]}
  - 立场 B：{argument + supporters [refs]}

---

## 8. Practical Implications

### 8.1 对研究者
{应该投入哪些方向 / 避开哪些方向}

### 8.2 对工程师 / 应用方
{当前可用的方法 + 选择指南}

### 8.3 对决策者
{这个领域的成熟度和落地时间窗}

---

## 9. Limitations of This Review

{诚实标注本综述的限制}：
- 覆盖时间窗
- 排除的子领域 / 语言
- 信源偏向（如：以英文文献为主）
- 评测方法的局限

---

## 10. References

按 APA 7th 格式，按字母排序：

```
1. Author, A., & Author, B. (2023). Title of paper. *Conference Name*. https://...
2. Author, C. (2024). Title. *arXiv*. https://arxiv.org/abs/...
3. ...
```

或 BibTeX 格式（如目标读者是研究者）：
```bibtex
@inproceedings{author2023title,
  title={Title of paper},
  author={Author, A. and Author, B.},
  booktitle={Conference Name},
  year={2023}
}
```

---

## 附录

### A. 时间线（可选可视化）
{ASCII timeline / 关键论文按年份排}

### B. 引用网络（可选）
{论文之间的引用关系}

### C. 检索策略
- 搜索 query：{list}
- 数据库：{list}
- Cut-off date：{YYYY-MM-DD}
```

---

## 关键写作规则

1. **每篇论文必须有 venue + 年份 + 引用数** —— 让读者快速判断重要性
2. **必须区分 "已被广泛接受" vs "争议中"** —— 学界共识 vs 争议要 surface
3. **必须含 open problems** —— 综述没 future directions 没意义
4. **必须含 limitations of this review** —— 学术诚实性
5. **arXiv-only 论文必须标注** —— 区分 peer-reviewed vs preprint
6. **Methods Comparison 表必须有** —— 横向对比是综述的核心价值
7. **Taxonomy 必须给来源** —— 是抄某 survey 的还是自己综合的要说清楚
