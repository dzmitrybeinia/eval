#!/usr/bin/env python3
"""Run cross-language error pattern analysis."""

import argparse
from typing import List

if __package__ in (None, ""):
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    if str(root) not in sys.path:
        sys.path.append(str(root))
    from toolkit import ErrorPatternAnalyzer, IssueAggregator  # type: ignore
else:
    from . import ErrorPatternAnalyzer, IssueAggregator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze recurring localization error patterns.")
    parser.add_argument(
        "--language",
        "-l",
        action="append",
        dest="languages",
        help="Language to analyze (repeatable). If omitted, all available languages with combined issues are processed.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    languages: List[str] | None = args.languages
    aggregator = IssueAggregator()
    targets: List[str] | None

    if languages is None:
        aggregated = aggregator.aggregate()
        targets = aggregated or None
    else:
        aggregated = aggregator.aggregate(languages)
        targets = aggregated or None

    if targets is not None and not aggregated:
        print("⚠️  No issues aggregated. Ensure evaluation results exist.")
        return

    analyzer = ErrorPatternAnalyzer()
    processed = analyzer.analyze(targets)
    if not processed:
        print("⚠️  No languages analyzed. Ensure issues data exists.")


if __name__ == "__main__":
    main()
