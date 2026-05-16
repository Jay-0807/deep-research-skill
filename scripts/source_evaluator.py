#!/usr/bin/env python3
"""
source_evaluator.py — 信源可信度评分脚本

读 sources.json（或从 markdown 报告里提取所有 URL），按 methodology/source-tiers.md
的规则给每条来源打 Tier。

输出：
- 标记为 Tier A / B / C / D
- 文本或 JSON 报告
- 给出每个 URL 的得分明细 + Tier
- 全局健康度（Tier A/B 占比、警告项）

用法：
    python source_evaluator.py <sources.json>
    python source_evaluator.py --from-md <report.md>     # 直接从报告里提取 URL
    python source_evaluator.py --json --from-md report.md

退出码：
    0  健康（Tier C 比例 ≤50% 且 Tier A+B ≥3）
    1  不健康（需补 Tier A/B 源）
    2  脚本错误 / 输入无效
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from urllib.parse import urlparse


URL_RE = re.compile(r"https?://[^\s)]+")


TIER_A_DOMAINS = {
    # academic
    "arxiv.org", "openalex.org", "semanticscholar.org", "doi.org",
    "pubmed.ncbi.nlm.nih.gov", "nature.com", "science.org", "cell.com",
    "ieee.org", "acm.org", "openreview.net", "neurips.cc", "aclanthology.org",
    "jmlr.org", "papers.nips.cc",
    # primary / government / official statistics
    "sec.gov", "ec.europa.eu", "oecd.org", "imf.org", "worldbank.org",
    "bls.gov", "census.gov", "ons.gov.uk", "europa.eu",
    "stats.gov.cn", "miit.gov.cn", "ndrc.gov.cn", "pbc.gov.cn",
    "drc.gov.cn", "creditchina.gov.cn", "gsxt.gov.cn",
    "caict.ac.cn", "cnnic.net.cn",
    # CB Insights / NBER / SSRN
    "nber.org", "ssrn.com",
    "cninfo.com.cn",  # 巨潮（A 股披露）
    "hkexnews.hk",     # 港交所披露
}

TIER_B_DOMAINS = {
    # research firms
    "gartner.com", "forrester.com", "idc.com", "mckinsey.com", "bain.com",
    "bcg.com", "deloitte.com", "pwc.com", "strategyand.pwc.com",
    "statista.com", "ibisworld.com", "cbinsights.com", "pitchbook.com",
    # quality media
    "ft.com", "wsj.com", "bloomberg.com", "reuters.com", "economist.com",
    "hbr.org", "theinformation.com", "stratechery.com", "a16z.com",
    # CN quality media / research
    "caixin.com", "latepost.com", "36kr.com", "geekpark.net",
    "iresearch.com.cn", "analysys.cn", "leadleo.com", "iyiou.com",
    "itjuzi.com", "qbitai.com", "jiqizhixin.com", "leiphone.com",
    "tisi.org", "aliresearch.com",
    # data / patents
    "crunchbase.com", "opencorporates.com", "patents.google.com",
    "cnipa.gov.cn",  # 国家知识产权局
    # tier-A-leaning corporate filings databases
    "qcc.com", "tianyancha.com", "qixin.com",
    # github / package registries (treated as evidence sources)
    "github.com",
    # other reputable
    "lennysnewsletter.com", "review.firstround.com",
    "huxiu.com", "tmtpost.com", "techcrunch.com",
}

TIER_C_DOMAINS = {
    "wired.com", "venturebeat.com", "theverge.com",
    "zhihu.com", "weibo.com", "v2ex.com",
    "medium.com", "substack.com",
    "reddit.com", "news.ycombinator.com",
    "g2.com", "capterra.com", "producthunt.com",
    "stackoverflow.com",
    "linkedin.com",  # posts are mixed quality
    "csdn.net", "juejin.cn", "infoq.cn", "ithome.com",
}

TIER_D_DOMAINS = {
    # known low-quality / SEO content farms / unmoderated
    "baijiahao.baidu.com",
    "163.com",
    "sohu.com",
    "sina.com.cn",
    # generic UGC w/o moderation
    "douban.com",
    "xiaohongshu.com",  # high-noise UGC; raw quotes can be useful but not authoritative
    "tieba.baidu.com",
}


@dataclass
class SourceScore:
    url: str
    domain: str
    tier: str = "C"
    score: int = 0
    reasons: list[str] = field(default_factory=list)


def normalize_domain(url: str) -> str:
    try:
        host = urlparse(url).hostname or ""
        # strip www. and common subdomains
        host = host.lower()
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


def domain_matches(host: str, whitelist: set[str]) -> str | None:
    """Match host or any parent domain against whitelist. Return matched entry."""
    parts = host.split(".")
    for i in range(len(parts)):
        candidate = ".".join(parts[i:])
        if candidate in whitelist:
            return candidate
    return None


def score_url(url: str) -> SourceScore:
    domain = normalize_domain(url)
    s = SourceScore(url=url, domain=domain)

    matched_a = domain_matches(domain, TIER_A_DOMAINS)
    matched_b = domain_matches(domain, TIER_B_DOMAINS)
    matched_c = domain_matches(domain, TIER_C_DOMAINS)
    matched_d = domain_matches(domain, TIER_D_DOMAINS)

    if matched_a:
        s.score += 3
        s.reasons.append(f"Tier A whitelist ({matched_a})")
    elif matched_b:
        s.score += 2
        s.reasons.append(f"Tier B whitelist ({matched_b})")
    elif matched_c:
        s.score += 1
        s.reasons.append(f"Tier C whitelist ({matched_c})")
    elif matched_d:
        s.score -= 2
        s.reasons.append(f"Tier D blacklist ({matched_d})")

    if url.startswith("https://"):
        s.score += 1
        s.reasons.append("HTTPS")

    if any(seg in domain for seg in (".gov", ".edu", ".ac.")):
        s.score += 1
        s.reasons.append("authoritative TLD")

    # tier mapping from score
    if s.score >= 4:
        s.tier = "A"
    elif s.score >= 2:
        s.tier = "B"
    elif s.score >= 0:
        s.tier = "C"
    else:
        s.tier = "D"

    # explicit overrides
    if matched_a:
        s.tier = "A"
    elif matched_d and s.tier in ("B", "C"):
        s.tier = "D"

    return s


def from_json(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    urls: list[str] = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                urls.append(item)
            elif isinstance(item, dict) and "url" in item:
                urls.append(item["url"])
    elif isinstance(data, dict) and "sources" in data:
        for item in data["sources"]:
            if isinstance(item, dict) and "url" in item:
                urls.append(item["url"])
    return urls


def from_markdown(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    urls = list(set(URL_RE.findall(text)))
    return urls


def evaluate(urls: list[str]) -> dict:
    scores = [score_url(u) for u in urls]
    by_tier = {"A": 0, "B": 0, "C": 0, "D": 0}
    for s in scores:
        by_tier[s.tier] += 1
    total = len(scores) or 1
    ab_share = (by_tier["A"] + by_tier["B"]) / total
    c_share = by_tier["C"] / total
    d_share = by_tier["D"] / total
    healthy = (by_tier["A"] + by_tier["B"]) >= 3 and c_share <= 0.5 and d_share <= 0.2
    return {
        "total": len(scores),
        "by_tier": by_tier,
        "ab_share": round(ab_share, 3),
        "c_share": round(c_share, 3),
        "d_share": round(d_share, 3),
        "healthy": healthy,
        "scores": [asdict(s) for s in scores],
    }


def print_text(result: dict) -> None:
    print("\n=== source_evaluator.py ===")
    print(f"Total sources:    {result['total']}")
    print(f"Tier A:           {result['by_tier']['A']}")
    print(f"Tier B:           {result['by_tier']['B']}")
    print(f"Tier C:           {result['by_tier']['C']}")
    print(f"Tier D:           {result['by_tier']['D']}")
    print(f"A+B share:        {result['ab_share']:.0%}")
    print(f"C share:          {result['c_share']:.0%}")
    print(f"D share:          {result['d_share']:.0%}")
    print(f"Overall healthy:  {'✓' if result['healthy'] else '✗'}")
    if not result["healthy"]:
        print("\nReasons to fail:")
        if (result["by_tier"]["A"] + result["by_tier"]["B"]) < 3:
            print(f"  - need ≥3 Tier A/B sources, have {result['by_tier']['A'] + result['by_tier']['B']}")
        if result["c_share"] > 0.5:
            print(f"  - Tier C share {result['c_share']:.0%} > 50%; supplement with higher-tier sources")
        if result["d_share"] > 0.2:
            print(f"  - Tier D share {result['d_share']:.0%} > 20%; remove or downweight unreliable sources")
    print("\nTier D sources (review):")
    for s in result["scores"]:
        if s["tier"] == "D":
            print(f"  ✗ {s['url']} ({', '.join(s['reasons']) or 'no whitelist match'})")


def main() -> int:
    ap = argparse.ArgumentParser(description="Score sources by tier.")
    ap.add_argument("input", type=Path, help="sources.json or report.md")
    ap.add_argument("--from-md", action="store_true", help="treat input as markdown")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.input.exists():
        print(f"[error] not found: {args.input}", file=sys.stderr)
        return 2
    urls = from_markdown(args.input) if args.from_md else from_json(args.input)
    if not urls:
        print("[error] no URLs extracted", file=sys.stderr)
        return 2
    result = evaluate(urls)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    return 0 if result["healthy"] else 1


if __name__ == "__main__":
    sys.exit(main())
