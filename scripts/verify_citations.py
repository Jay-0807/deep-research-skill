#!/usr/bin/env python3
"""
verify_citations.py — 引用反幻觉校验脚本

扫描调研报告里的所有 URL / DOI 引用，验证：
1. URL 是否可访问（HTTP 200 / 302）
2. DOI 是否能在 doi.org / crossref 解析
3. 引用的标题与页面 <title> 是否大致匹配（防 URL 张冠李戴）
4. 是否有"看似引用但无 URL"的可疑 claim

用法：
    python verify_citations.py <report.md>
    python verify_citations.py --strict <report.md>    # 严格模式：标题不匹配也 fail
    python verify_citations.py --json <report.md>      # JSON 输出

退出码：
    0  全部通过
    1  发现可修复问题
    2  脚本错误 / 输入无效

依赖：requests, beautifulsoup4 (`pip install requests beautifulsoup4`)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[error] missing deps. run: pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(2)


MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+\b")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (verify_citations.py) deep-research/1.0",
    "Accept-Language": "en,zh-CN;q=0.9",
}
TIMEOUT = 15


@dataclass
class CitationCheck:
    text: str
    url: str
    status: int = 0
    final_url: str = ""
    page_title: str = ""
    text_match: bool = True
    error: str = ""

    @property
    def ok(self) -> bool:
        return (200 <= self.status < 400) and not self.error


@dataclass
class Report:
    file: str
    total_links: int = 0
    ok_count: int = 0
    fail_count: int = 0
    dois: list[str] = field(default_factory=list)
    failures: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def extract_citations(text: str) -> list[tuple[str, str]]:
    """Return list of (anchor_text, url) tuples for all markdown links."""
    return MD_LINK_RE.findall(text)


def extract_dois(text: str) -> list[str]:
    return sorted(set(DOI_RE.findall(text)))


def normalize_for_match(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def title_matches(anchor: str, page_title: str) -> bool:
    """Loose match — anchor 至少与 page title 有显著词重叠。"""
    if not page_title:
        return True  # cannot judge
    a = normalize_for_match(anchor)
    t = normalize_for_match(page_title)
    if len(a) < 6:
        return True  # anchor too short to judge
    if a in t or t.startswith(a[:20]):
        return True
    a_tokens = set(re.findall(r"\w{3,}", a))
    t_tokens = set(re.findall(r"\w{3,}", t))
    if not a_tokens:
        return True
    overlap = len(a_tokens & t_tokens) / max(len(a_tokens), 1)
    return overlap >= 0.3


def check_url(anchor: str, url: str) -> CitationCheck:
    chk = CitationCheck(text=anchor, url=url)
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        chk.status = r.status_code
        chk.final_url = r.url
        if r.status_code >= 400:
            chk.error = f"HTTP {r.status_code}"
            return chk
        ct = r.headers.get("Content-Type", "")
        if "text/html" in ct.lower() and r.text:
            soup = BeautifulSoup(r.text[:200_000], "html.parser")
            t = soup.find("title")
            if t and t.text:
                chk.page_title = t.text.strip()[:300]
        chk.text_match = title_matches(anchor, chk.page_title)
    except requests.RequestException as e:
        chk.error = f"{type(e).__name__}: {e}"
    return chk


def check_doi(doi: str) -> CitationCheck:
    url = f"https://doi.org/{doi}"
    chk = check_url(f"DOI:{doi}", url)
    return chk


def run(path: Path, strict: bool) -> Report:
    text = path.read_text(encoding="utf-8")
    report = Report(file=str(path))
    citations = extract_citations(text)
    dois = extract_dois(text)
    report.dois = dois
    report.total_links = len(citations)

    seen_urls: set[str] = set()
    for anchor, url in citations:
        if url in seen_urls:
            continue
        seen_urls.add(url)
        chk = check_url(anchor, url)
        if chk.ok and (chk.text_match or not strict):
            report.ok_count += 1
        else:
            report.fail_count += 1
            report.failures.append(
                {
                    "anchor": anchor,
                    "url": url,
                    "status": chk.status,
                    "page_title": chk.page_title,
                    "text_match": chk.text_match,
                    "error": chk.error,
                }
            )

    for doi in dois:
        chk = check_doi(doi)
        if not chk.ok:
            report.fail_count += 1
            report.failures.append(
                {
                    "anchor": f"DOI {doi}",
                    "url": chk.url,
                    "status": chk.status,
                    "error": chk.error or "DOI not resolvable",
                }
            )

    # heuristic: claims with "[N]" reference markers but no URL anywhere nearby
    bracket_refs = re.findall(r"\[\d+\]", text)
    if bracket_refs and report.total_links < len(bracket_refs):
        report.warnings.append(
            f"Found {len(bracket_refs)} numbered refs but only {report.total_links} URLs — some refs may be missing URLs."
        )

    return report


def print_text(report: Report) -> None:
    print(f"\n=== verify_citations.py: {report.file} ===")
    print(f"Total markdown links: {report.total_links}")
    print(f"  ok:   {report.ok_count}")
    print(f"  fail: {report.fail_count}")
    print(f"DOIs found:           {len(report.dois)}")
    if report.warnings:
        print("\nWarnings:")
        for w in report.warnings:
            print(f"  ⚠ {w}")
    if report.failures:
        print("\nFailures (must fix):")
        for f in report.failures:
            print(f"  ✗ [{f['anchor']}]({f['url']})")
            if f.get("status"):
                print(f"     status={f['status']}")
            if f.get("page_title"):
                print(f"     page_title={f['page_title']!r}")
            if f.get("text_match") is False:
                print("     text/title mismatch — possible wrong URL")
            if f.get("error"):
                print(f"     error={f['error']}")
    else:
        print("\nAll citations OK ✓")


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify citations in a research markdown report.")
    ap.add_argument("report", type=Path, help="path to report.md")
    ap.add_argument("--strict", action="store_true", help="fail on title mismatch")
    ap.add_argument("--json", action="store_true", help="output machine-readable JSON")
    args = ap.parse_args()

    if not args.report.exists():
        print(f"[error] not found: {args.report}", file=sys.stderr)
        return 2

    report = run(args.report, strict=args.strict)

    if args.json:
        print(json.dumps(report.__dict__, ensure_ascii=False, indent=2, default=str))
    else:
        print_text(report)

    return 1 if report.fail_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
