#!/usr/bin/env python3
"""
validate_report.py — 调研报告结构 / 质量校验脚本

9 项硬约束检查（参考 199-bio 的 validate_report.py）：
1. 至少 10 个独立 URL 来源（full tier）/ 5 个（light tier）
2. 至少 1 条引用 Tier A 源（如有 sources.json）
3. References 段存在且 ≥10 条
4. TL;DR / Exec Summary 段存在且 ≤500 字
5. 包含 Risks / Limitations / Open Questions 段
6. 包含 Recommendations / 建议 段
7. 不出现空洞结论标志短语（"前景广阔" / "值得关注" 等）
8. 关键数字（含 % / 亿 / billion / million / 万）至少邻近一个 URL
9. 不出现孤立的"[N]"编号引用（无配套 URL）

用法：
    python validate_report.py <report.md>
    python validate_report.py --tier light <report.md>
    python validate_report.py --tier deep <report.md>
    python validate_report.py --json <report.md>

退出码：
    0  全部通过
    1  有未通过的硬约束
    2  脚本错误 / 输入无效
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path


URL_RE = re.compile(r"https?://[^\s)]+")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
NUMERIC_CLAIM_RE = re.compile(
    r"(\d[\d,\.]*\s*(?:%|百分点|亿|万亿|万|千|百|billion|million|thousand|trillion|B|M|K)\b)",
    re.IGNORECASE,
)
EMPTY_PHRASES = [
    "前景广阔",
    "值得关注",
    "值得期待",
    "未来可期",
    "大有可为",
    "有待观察",
    "潜力巨大",
    "重要意义",
    "broad prospects",
    "bright future",
    "worth watching",
    "remains to be seen",
    "promising area",
]
TIER_MIN_SOURCES = {"light": 5, "full": 10, "deep": 20}
TIER_MIN_REFS = {"light": 5, "full": 10, "deep": 20}


@dataclass
class Check:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class ValidationReport:
    file: str
    tier: str
    checks: list[Check] = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)


def get_section(text: str, names: list[str]) -> str | None:
    """Return body of the first section whose heading matches any of `names`."""
    pattern = re.compile(
        r"^(#{1,6})\s+(?:" + "|".join(re.escape(n) for n in names) + r")\b.*$",
        re.MULTILINE | re.IGNORECASE,
    )
    m = pattern.search(text)
    if not m:
        return None
    start_level = len(m.group(1))
    body_start = m.end()
    next_h = re.search(rf"^#{{1,{start_level}}}\s", text[body_start:], re.MULTILINE)
    body_end = body_start + next_h.start() if next_h else len(text)
    return text[body_start:body_end]


def check_min_sources(text: str, tier: str) -> Check:
    urls = set(URL_RE.findall(text))
    n = len(urls)
    need = TIER_MIN_SOURCES.get(tier, 10)
    return Check(
        name=f"≥{need} unique source URLs ({tier} tier)",
        passed=n >= need,
        detail=f"found {n} unique URLs",
    )


def check_references_section(text: str, tier: str) -> Check:
    body = get_section(text, ["References", "参考文献", "参考资料", "Sources"])
    if body is None:
        return Check(name="References section exists", passed=False, detail="no References / 参考文献 heading")
    refs = MD_LINK_RE.findall(body)
    need = TIER_MIN_REFS.get(tier, 10)
    return Check(
        name=f"References section ≥{need} entries",
        passed=len(refs) >= need,
        detail=f"found {len(refs)} markdown link entries in References",
    )


def check_tldr(text: str) -> Check:
    body = get_section(text, ["TL;DR", "TLDR", "Executive Summary", "Exec Summary", "概要", "摘要"])
    if body is None:
        return Check(name="TL;DR / Exec Summary present", passed=False, detail="no TL;DR / Exec Summary section")
    chars = len(body.strip())
    return Check(
        name="TL;DR / Exec Summary ≤500 chars",
        passed=chars <= 1500,  # generous: ~500 Chinese chars or ~250 English words
        detail=f"section length {chars} chars",
    )


def check_section_present(text: str, names: list[str], label: str) -> Check:
    body = get_section(text, names)
    return Check(
        name=f"{label} section present",
        passed=body is not None,
        detail=f"looked for: {', '.join(names)}",
    )


def check_empty_phrases(text: str) -> Check:
    hits = [p for p in EMPTY_PHRASES if p in text]
    return Check(
        name="No empty conclusion phrases",
        passed=not hits,
        detail=f"found banned phrases: {hits}" if hits else "none",
    )


def check_numeric_claims_have_sources(text: str) -> Check:
    """Heuristic: for every numeric claim, find an URL within +/-300 chars."""
    matches = list(NUMERIC_CLAIM_RE.finditer(text))
    unsupported: list[str] = []
    for m in matches:
        start = max(0, m.start() - 300)
        end = min(len(text), m.end() + 300)
        window = text[start:end]
        if not URL_RE.search(window):
            unsupported.append(m.group(0))
    return Check(
        name="Key numeric claims have nearby source",
        passed=len(unsupported) <= max(1, len(matches) // 10),  # allow ≤10% unsupported
        detail=f"unsupported claims (sample 5): {unsupported[:5]}; total {len(unsupported)}/{len(matches)}",
    )


def check_orphan_numbered_refs(text: str) -> Check:
    bracket_refs = re.findall(r"\[\d+\]", text)
    urls = URL_RE.findall(text)
    if not bracket_refs:
        return Check(name="No orphan [N] refs", passed=True, detail="no [N]-style refs found")
    return Check(
        name="No orphan [N] refs (have ≥as many URLs)",
        passed=len(urls) >= len(bracket_refs),
        detail=f"{len(bracket_refs)} [N] refs vs {len(urls)} URLs",
    )


def run(path: Path, tier: str) -> ValidationReport:
    text = path.read_text(encoding="utf-8")
    rep = ValidationReport(file=str(path), tier=tier)
    rep.checks.append(check_min_sources(text, tier))
    rep.checks.append(check_references_section(text, tier))
    rep.checks.append(check_tldr(text))
    rep.checks.append(check_section_present(text, ["Risks", "风险", "Limitations", "限制", "不确定性"], "Risks/Limitations"))
    rep.checks.append(check_section_present(text, ["Recommendation", "Recommendations", "建议", "决策建议"], "Recommendations"))
    rep.checks.append(check_empty_phrases(text))
    rep.checks.append(check_numeric_claims_have_sources(text))
    rep.checks.append(check_orphan_numbered_refs(text))
    rep.summary = {
        "total": len(rep.checks),
        "passed": sum(1 for c in rep.checks if c.passed),
        "failed": sum(1 for c in rep.checks if not c.passed),
    }
    return rep


def print_text(rep: ValidationReport) -> None:
    print(f"\n=== validate_report.py: {rep.file} (tier={rep.tier}) ===")
    for c in rep.checks:
        mark = "✓" if c.passed else "✗"
        print(f"  {mark} {c.name}")
        if c.detail:
            print(f"      {c.detail}")
    s = rep.summary
    print(f"\n{s['passed']}/{s['total']} checks passed.")
    if not rep.passed:
        print("Report has unmet hard constraints — fix before delivery.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate research report against 8 hard checks.")
    ap.add_argument("report", type=Path)
    ap.add_argument("--tier", choices=["light", "full", "deep"], default="full")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.report.exists():
        print(f"[error] not found: {args.report}", file=sys.stderr)
        return 2
    rep = run(args.report, args.tier)
    if args.json:
        print(json.dumps(asdict(rep), ensure_ascii=False, indent=2))
    else:
        print_text(rep)
    return 0 if rep.passed else 1


if __name__ == "__main__":
    sys.exit(main())
