"""
Silent Reviewer — CLI version
Usage: python cli.py <file>
       python cli.py mycode.py
"""

import sys
import os
from reviewer import review_code

RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
GREEN  = "\033[92m"
PURPLE = "\033[95m"
MUTED  = "\033[90m"
CYAN   = "\033[96m"


def color_severity(s):
    return RED if s == "critical" else YELLOW if s == "warning" else BLUE


def print_issues(issues, category_icon):
    if not issues:
        print(f"    {GREEN}✓ No issues found{RESET}")
        return
    for i in issues:
        col = color_severity(i.severity)
        line_str = f" (line {i.line})" if i.line else ""
        conf_str = f"{MUTED}[{i.confidence}% confidence]{RESET}"
        print(f"    {col}● {i.severity.upper()}{RESET}{line_str} {conf_str}")
        print(f"      {i.message}")
        if i.fix:
            print(f"      {GREEN}→ Fix: {i.fix}{RESET}")
        print()


def main():
    if len(sys.argv) < 2:
        print(f"{BOLD}Usage:{RESET} python cli.py <filename>")
        print(f"  python cli.py mycode.py")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"{RED}File not found: {filepath}{RESET}")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    filename = os.path.basename(filepath)

    try:
        result = review_code(code, filename)
    except RuntimeError as e:
        print(f"\n{RED}{e}{RESET}")
        sys.exit(1)

    summary = result["summary"]
    agents  = result["agents"]

    print(f"\n{BOLD}{PURPLE}{'─'*55}")
    print(f"  SILENT REVIEWER — FINAL REPORT")
    print(f"{'─'*55}{RESET}")

    # Score
    score = summary.get("overall_score", 0)
    grade = summary.get("grade", "?")
    score_col = GREEN if score >= 80 else YELLOW if score >= 60 else RED
    print(f"\n  {BOLD}Score:{RESET} {score_col}{score}/100  Grade {grade}{RESET}")
    print(f"  {BOLD}File: {RESET}{filename}  ({result['line_count']} lines, {result['language']})")
    print(f"\n  {summary.get('verdict', '')}")
    print(f"\n  {YELLOW}⚡ Top priority:{RESET} {summary.get('top_priority', '')}")
    if summary.get("strengths"):
        print(f"  {GREEN}✓ Strengths:{RESET} {summary.get('strengths', '')}")

    # Per-agent
    sections = [
        ("bugs",        "🐛 BUG HUNTER"),
        ("security",    "🔒 SECURITY SCANNER"),
        ("performance", "⚡ PERFORMANCE"),
        ("style",       "✨ STYLE & PRACTICES"),
    ]

    for key, label in sections:
        agent = agents[key]
        issues = agent.issues
        count = len(issues)
        print(f"\n{BOLD}{CYAN}  {label}{RESET}  {MUTED}({count} issue{'s' if count!=1 else ''}){RESET}")
        if agent.error:
            print(f"    {YELLOW}⚠ Agent error: {agent.error}{RESET}")
        else:
            print_issues(issues, label[0])

    # Disclaimer
    print(f"{MUTED}{'─'*55}")
    print(f"  ⚠ {summary.get('model_disclaimer', '')}")
    print(f"{'─'*55}{RESET}\n")


if __name__ == "__main__":
    main()
