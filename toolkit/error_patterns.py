"""Error pattern analysis helpers using Azure OpenAI."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from dotenv import load_dotenv
from openai import AzureOpenAI


class ErrorPatternAnalyzer:
    """Generate cross-language error pattern reports."""

    SEVERITIES = ("HIGH", "MEDIUM", "MINOR")
    CATEGORIES = ("linguistic", "localization")

    def __init__(
        self,
        base_dir: Path | str = ".",
        prompt_path: Path | str = "prompts/error_pattern_analysis.md",
    ) -> None:
        load_dotenv()
        self.base_path = Path(base_dir)
        self.issues_dir = self.base_path / "issues"
        self.output_dir = self.issues_dir / "all"
        self.patterns_dir = self.issues_dir / "common_patterns"
        self.prompt_path = Path(prompt_path)
        self.prompt_template = self._load_prompt()
        self.client = AzureOpenAI(
            azure_endpoint=self._require_env("ENDPOINT_URL"),
            api_key=self._require_env("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("API_VERSION", "2025-01-01-preview"),
        )
        self.deployment = os.getenv("DEPLOYMENT_NAME", "o3-mini")

    def analyze(self, languages: Iterable[str] | None = None) -> List[str]:
        languages_to_process = list(languages or self._discover_languages())
        processed: List[str] = []
        analyses: Dict[str, Dict] = {}

        for language in languages_to_process:
            combined_issues = self._load_combined_issues(language)
            if combined_issues is None:
                continue

            reports = self._analyze_language(language, combined_issues)
            if not reports:
                continue

            merged = self._merge(reports)
            analyses[language] = merged
            self._write_language_report(language, merged)
            processed.append(language)

        if analyses:
            self._write_global_report(analyses)

        return processed

    def _analyze_language(self, language: str, combined_issues: Dict[str, List[Dict]]) -> List[Dict]:
        reports: List[Dict] = []
        for category in self.CATEGORIES:
            for severity in self.SEVERITIES:
                issues = [
                    issue
                    for issue in combined_issues.get(category, [])
                    if issue.get("severity", "MEDIUM") == severity
                ]
                if not issues:
                    continue
                report = self._call_model(language, category, severity, issues)
                if report:
                    reports.append(report)
        return reports

    def _call_model(
        self,
        language: str,
        category: str,
        severity: str,
        issues: List[Dict],
    ) -> Optional[Dict]:
        prompt = (
            f"{self.prompt_template}\n\n"
            f"**Target language:** {language.title()}\n"
            f"**Pattern focus:** {category} issues with {severity} severity\n"
            f"**Issue count:** {len(issues)}\n\n"
            f"**Issues to analyse:**\n{json.dumps(issues, ensure_ascii=False, indent=2)}"
        )

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You are a localization quality expert. Return only valid JSON without markdown.",
                },
                {"role": "user", "content": prompt},
            ],
            max_completion_tokens=16_384,
            temperature=0.0,
        )
        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            try:
                cleaned = content.strip().strip("`")
                return json.loads(cleaned)
            except json.JSONDecodeError:
                print(f"⚠️  Failed to parse model output for {language} ({category}/{severity})")
                return None

    def _merge(self, reports: List[Dict]) -> Dict:
        if not reports:
            return {}

        merged_patterns = self._merge_patterns(reports)
        return {"top_error_patterns": merged_patterns}

    @staticmethod
    def _merge_patterns(reports: List[Dict]) -> List[Dict]:
        deduped: Dict[tuple[str, str], Dict] = {}
        severity_priority = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        frequency_priority = {"very_common": 4, "common": 3, "occasional": 2, "rare": 1}

        for report in reports:
            for pattern in report.get("top_error_patterns", []):
                name = pattern.get("pattern_name", "").strip()
                category = pattern.get("category", "")
                if not name:
                    continue

                key = (name, category)
                frequency_count = pattern.get("frequency_count")
                try:
                    frequency_count = int(frequency_count)
                except (TypeError, ValueError):
                    frequency_count = 0

                entry = deduped.get(key)
                if entry is None:
                    new_entry = {
                        "pattern_name": name,
                        "category": category,
                        "subcategory": pattern.get("subcategory", ""),
                        "impact_level": pattern.get("impact_level", "MEDIUM"),
                        "frequency": pattern.get("frequency", "common"),
                        "frequency_count": frequency_count,
                        "description": pattern.get("description", ""),
                        "examples": pattern.get("examples", []) or [],
                    }
                    deduped[key] = new_entry
                    continue

                entry["frequency_count"] += frequency_count

                current_severity = entry.get("impact_level", "MEDIUM")
                new_severity = pattern.get("impact_level", "MEDIUM")
                if severity_priority.get(new_severity, 2) > severity_priority.get(current_severity, 2):
                    entry["impact_level"] = new_severity

                current_freq = entry.get("frequency", "common")
                new_freq = pattern.get("frequency", current_freq)
                if frequency_priority.get(new_freq, 0) > frequency_priority.get(current_freq, 0):
                    entry["frequency"] = new_freq

                if not entry.get("description") and pattern.get("description"):
                    entry["description"] = pattern.get("description", "")

                examples = pattern.get("examples", []) or []
                if examples:
                    existing_examples = {json.dumps(ex, sort_keys=True) for ex in entry.get("examples", [])}
                    for example in examples:
                        serialized = json.dumps(example, sort_keys=True)
                        if serialized not in existing_examples:
                            entry.setdefault("examples", []).append(example)
                            existing_examples.add(serialized)

        patterns = list(deduped.values())
        patterns.sort(
            key=lambda p: (
                severity_priority.get(p.get("impact_level", "MEDIUM"), 0),
                p.get("frequency_count", 0),
            ),
            reverse=True,
        )
        return patterns

    def _write_language_report(self, language: str, report: Dict) -> None:
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        out_path = self.patterns_dir / f"{language}.json"
        with open(out_path, "w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)
        print(f"📄 Saved analysis for {language}")

    def _write_global_report(self, analyses: Dict[str, Dict]) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        out_path = self.output_dir / "all_common_issues.json"

        existing: Dict[str, Dict] = {"languages": [], "analyses": {}}
        if out_path.exists():
            try:
                with open(out_path, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
                    if isinstance(data, dict):
                        existing = {
                            "languages": data.get("languages", []),
                            "analyses": data.get("analyses", {}),
                        }
            except (OSError, json.JSONDecodeError):
                pass

        merged_analyses = existing["analyses"]
        merged_analyses.update(analyses)
        languages = sorted(merged_analyses.keys())

        payload = {"languages": languages, "analyses": merged_analyses}

        with open(out_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        print("🌍 Saved aggregated common issues report")

    def _load_prompt(self) -> str:
        try:
            return self.prompt_path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Error pattern prompt not found: {self.prompt_path}") from exc

    def _load_combined_issues(self, language: str) -> Optional[Dict[str, List[Dict]]]:
        combined_path = self.issues_dir / "combined_issues" / f"{language}_issues.json"
        if not combined_path.exists():
            print(f"⏭️  Skipping {language} - run issue aggregation first")
            return None
        try:
            with open(combined_path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"⚠️  Could not read {combined_path.name}: {exc}")
            return None

    def _discover_languages(self) -> List[str]:
        combined_dir = self.issues_dir / "combined_issues"
        if not combined_dir.exists():
            return []
        languages = [
            path.stem.replace("_issues", "")
            for path in sorted(combined_dir.glob("*_issues.json"))
        ]
        return languages

    @staticmethod
    def _require_env(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise ValueError(f"{name} environment variable is required. Please check your .env file.")
        return value


__all__ = ["ErrorPatternAnalyzer"]
