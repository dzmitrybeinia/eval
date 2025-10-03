"""Issue aggregation utilities for evaluation outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List

from .constants import SUPPORTED_LANGUAGES


class IssueAggregator:
    """Aggregate linguistic and localization issues per language."""

    def __init__(self, base_dir: Path | str = ".") -> None:
        base_path = Path(base_dir)
        self.eval_results_dir = base_path / "eval_results"
        self.issues_dir = base_path / "issues"
        self.combined_dir = self.issues_dir / "combined_issues"

    def aggregate(self, languages: Iterable[str] | None = None) -> List[str]:
        languages_to_process = list(languages or self._discover_languages())
        processed: List[str] = []

        for language in languages_to_process:
            combined = self._collect_language_issues(language)
            if combined is None:
                continue
            self.combined_dir.mkdir(parents=True, exist_ok=True)
            output_file = self.combined_dir / f"{language}_issues.json"
            with open(output_file, "w", encoding="utf-8") as handle:
                json.dump(combined, handle, ensure_ascii=False, indent=2)
            print(f"🗂️  Aggregated issues for {language}")
            processed.append(language)

        return processed

    def _discover_languages(self) -> List[str]:
        if not self.eval_results_dir.exists():
            return []
        languages = [
            path.name
            for path in sorted(self.eval_results_dir.iterdir())
            if path.is_dir()
        ]
        return languages or [lang for lang in SUPPORTED_LANGUAGES if lang != "english"]

    def _collect_language_issues(self, language: str) -> Dict[str, List[Dict]] | None:
        language_dir = self.eval_results_dir / language
        if not language_dir.exists():
            print(f"⏭️  Skipping {language} - no evaluation results")
            return None

        combined: Dict[str, List[Dict]] = {"linguistic": [], "localization": []}

        for json_file in sorted(language_dir.glob("*.json")):
            try:
                with open(json_file, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
            except (OSError, json.JSONDecodeError) as exc:
                print(f"⚠️  Skipping {json_file.name} ({exc})")
                continue

            for issue in data.get("issues", []):
                category = issue.get("category")
                if category in combined:
                    combined[category].append(issue)

        return combined


__all__ = ["IssueAggregator"]
