"""Evaluation helpers built on Azure OpenAI."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from openai import AzureOpenAI

from .constants import SUPPORTED_LANGUAGES
from .error_patterns import ErrorPatternAnalyzer
from .issues import IssueAggregator
from .labels import LabelInfo, ensure_label
from .scoring import SimpleScorer

try:
    from prompts.prompt_builder import PromptBuilder
except ModuleNotFoundError as exc:  # pragma: no cover - misconfiguration guard
    raise RuntimeError("Missing prompts package. Ensure prompts/prompt_builder.py is available.") from exc


class QuizEvaluator:
    """Run localization quality evaluation over markdown quizzes."""

    def __init__(self, base_dir: Path | str = ".") -> None:
        self.client = AzureOpenAI(
            azure_endpoint=self._require_env("ENDPOINT_URL"),
            api_key=self._require_env("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("API_VERSION", "2025-01-01-preview"),
        )
        self.deployment = os.getenv("DEPLOYMENT_NAME", "o3-mini")

        base_path = Path(base_dir)
        self.markdown_dir = base_path / "markdown_quizzes"
        self.eval_results_dir = base_path / "eval_results"

        self.scorer = SimpleScorer()
        self.prompt_builder = PromptBuilder()
        self.issue_aggregator = IssueAggregator(base_path)
        self.pattern_analyzer = ErrorPatternAnalyzer(base_dir=base_path)

    def evaluate_language(self, language: str, label: LabelInfo | str) -> bool:
        label_info = ensure_label(label)
        source_dir = self.markdown_dir / language
        if not source_dir.exists():
            print(f"❌ Markdown directory not found: {source_dir}")
            return False

        language_dir = self.eval_results_dir / language
        language_dir.mkdir(parents=True, exist_ok=True)

        md_files = sorted(source_dir.glob("*.md"))
        if not md_files:
            print(f"❌ No markdown files found in {source_dir}")
            return False

        print(f"📁 Found {len(md_files)} markdown file(s) in {source_dir}")
        print(f"🏷️  Using label: {label_info.original}")
        evaluated = 0

        for md_file in md_files:
            print(f"🔄 Evaluating {md_file.name}...")
            if self.evaluate_file(md_file, language, label_info):
                evaluated += 1
                print(f"✅ Evaluated {md_file.name}")
            else:
                print(f"❌ Failed to evaluate {md_file.name}")

        print("\n📊 Evaluation Summary:")
        print(f"   ✅ Evaluated: {evaluated}")
        print(f"   📝 Total files: {len(md_files)}")

        success = evaluated > 0
        if success:
            self._refresh_file_index()
            self._update_issue_data(label_info, [language])
        return success

    def evaluate_all_languages(self, label: LabelInfo | str) -> bool:
        label_info = ensure_label(label)
        print("🌍 Starting evaluation for ALL supported languages")
        print(f"📋 Languages to process: {', '.join(lang.title() for lang in SUPPORTED_LANGUAGES)}")
        print(f"🏷️  Label: {label_info.original}")
        print("=" * 60)

        successful: list[str] = []
        failed: list[str] = []
        skipped: list[str] = []
        total_files = 0

        for index, language in enumerate(SUPPORTED_LANGUAGES, start=1):
            print(f"\n🔄 Processing language {index}/{len(SUPPORTED_LANGUAGES)}: {language.title()}")
            print("-" * 40)

            source_dir = self.markdown_dir / language
            if not source_dir.exists():
                print(f"⏭️  Skipping {language.title()} - no markdown directory found")
                skipped.append(language)
                continue

            md_files = list(source_dir.glob("*.md"))
            if not md_files:
                print(f"⏭️  Skipping {language.title()} - no markdown files found")
                skipped.append(language)
                continue

            if self.evaluate_language(language, label_info):
                successful.append(language)
                total_files += len(md_files)
            else:
                failed.append(language)

        print("\n" + "=" * 60)
        print("🎯 EVALUATION CYCLE COMPLETE")
        print("=" * 60)
        print(f"✅ Successfully processed: {len(successful)} languages")
        for lang in successful:
            print(f"   • {lang.title()}")

        if skipped:
            print(f"\n⏭️  Skipped: {len(skipped)} languages")
            for lang in skipped:
                print(f"   • {lang.title()}")

        if failed:
            print(f"\n❌ Failed: {len(failed)} languages")
            for lang in failed:
                print(f"   • {lang.title()}")

        print(f"\n📊 Total files evaluated: {total_files}")
        print(f"🏷️  Label used: {label_info.original}")

        if successful:
            self._update_issue_data(label_info, successful)

        return bool(successful)

    def evaluate_file(self, md_file: Path, language: str, label: LabelInfo) -> bool:
        try:
            with open(md_file, "r", encoding="utf-8") as handle:
                content = handle.read()
        except OSError as exc:  # noqa: BLE001 - surface IO errors
            print(f"Error reading {md_file}: {exc}")
            return False

        if language.lower() == "english":
            result = self._evaluate_single_step(content, language)
        else:
            result = self._evaluate_combined(content, language)

        if not result:
            return False

        evaluation_json = self._parse_response(result, md_file, language, label)
        if not evaluation_json:
            return False

        self._persist_evaluation(evaluation_json, language)
        return True

    def _evaluate_single_step(self, content: str, language: str) -> str:
        prompt = self.prompt_builder.build_prompt(language, content, step="single")
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert educational content evaluator specializing in quiz quality "
                        "assessment and localization review. You must return only valid JSON without any additional text."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_completion_tokens=32_768,
            temperature=0.0,
        )
        return response.choices[0].message.content.strip()

    def _evaluate_combined(self, content: str, language: str) -> str:
        print("🔬 Combined linguistic & localization analysis...")
        prompt = self.prompt_builder.build_prompt(language, content, step="combined")
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a specialized dual-expertise evaluator combining both linguistic accuracy and "
                        "localization quality assessment. Apply deduplication rules strictly. Return only valid JSON "
                        "without any additional text."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_completion_tokens=32_768,
            temperature=0.0,
        )
        print("✅ Combined analysis completed")
        return response.choices[0].message.content.strip()

    def _parse_response(
        self,
        response_text: str,
        md_file: Path,
        language: str,
        label: LabelInfo,
    ) -> Optional[Dict]:
        cleaned = self._clean_json_response(response_text)
        try:
            evaluation_json = json.loads(cleaned)
        except json.JSONDecodeError as err:
            print(f"⚠️  JSON parsing failed: {err}")
            print(f"Raw response (first 500 chars): {response_text[:500]}...")
            print(f"Raw response (last 200 chars): ...{response_text[-200:]}")
            print(f"🧹 Cleaned response length: {len(cleaned)} chars")
            evaluation_json = self._fallback_parse(response_text)
            if evaluation_json is None:
                print("❌ All JSON extraction attempts failed")
                return None
            print("✅ Successfully extracted JSON using fallback strategy")

        if "issues" not in evaluation_json or not isinstance(evaluation_json["issues"], list):
            print("⚠️  Invalid format: 'issues' must be an array")
            return None

        evaluation_json.setdefault("metadata", {})
        metadata = evaluation_json["metadata"]
        metadata.update(
            {
                "file": md_file.name,
                "language": language.title(),
                "timestamp": datetime.now().isoformat(),
                "model": "gpt 4.1",
            }
        )
        metadata["label"] = label.original

        scores = self.scorer.calculate_score(evaluation_json.get("issues", []))
        evaluation_json["scores"] = scores
        print(
            "📊 Calculated scores - Overall: "
            f"{scores['overall_quality_score']}/10 ({scores['classification']})"
        )
        return evaluation_json

    def _persist_evaluation(self, evaluation_json: Dict, language: str) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_filename = f"evaluation_{timestamp}.json"
        result_path = self.eval_results_dir / language / result_filename
        with open(result_path, "w", encoding="utf-8") as handle:
            json.dump(evaluation_json, handle, indent=2, ensure_ascii=False)
        print(f"💾 Evaluation saved: {result_filename}")

    def _update_issue_data(self, label: LabelInfo, languages: List[str]) -> None:
        if not languages:
            return

        try:
            aggregated = self.issue_aggregator.aggregate(languages, label=label)
        except Exception as exc:  # noqa: BLE001 - surface dependency failures gracefully
            print(f"⚠️  Issue aggregation failed for label '{label.original}': {exc}")
            return

        if not aggregated:
            print(f"⚠️  Issue aggregation produced no data for label '{label.original}'.")
            return

        try:
            processed = self.pattern_analyzer.analyze(aggregated, label=label)
        except Exception as exc:  # noqa: BLE001 - surface dependency failures gracefully
            print(f"⚠️  Issue pattern analysis failed for label '{label.original}': {exc}")
            return

        if not processed:
            print(f"⚠️  No common issue patterns generated for label '{label.original}'.")

    def refresh_file_index(self) -> None:
        """Rebuild the dashboard file index without running evaluations."""
        self._refresh_file_index()

    def _refresh_file_index(self) -> None:
        index_data = self._build_file_index()
        if not index_data:
            return

        index_path = self.eval_results_dir.parent / "file_index.json"
        with open(index_path, "w", encoding="utf-8") as handle:
            json.dump(index_data, handle, indent=2, ensure_ascii=False)
        print(f"📄 Updated file index: {index_path.name}")

    def _build_file_index(self) -> Optional[Dict[str, object]]:
        if not self.eval_results_dir.exists():
            return None

        language_files: Dict[str, List[str]] = {}
        total_files = 0

        for language_dir in sorted(self.eval_results_dir.iterdir()):
            if not language_dir.is_dir():
                continue

            files_with_mtime: List[tuple[str, float]] = []
            for json_file in language_dir.glob("*.json"):
                if not json_file.is_file():
                    continue
                try:
                    mtime = json_file.stat().st_mtime
                except OSError:
                    mtime = 0
                files_with_mtime.append((json_file.name, mtime))

            if files_with_mtime:
                files_with_mtime.sort(key=lambda item: item[1], reverse=True)
                language_files[language_dir.name] = [name for name, _ in files_with_mtime]
                total_files += len(files_with_mtime)

        return {
            "generated_at": datetime.now().isoformat(),
            "total_files": total_files,
            "languages": sorted(language_files.keys()),
            "files": language_files,
        }

    def _fallback_parse(self, response_text: str) -> Optional[Dict]:
        strategies = (
            self._extract_json_by_braces,
            self._aggressive_clean_and_parse,
            self._extract_json_by_issues_pattern,
        )
        for index, strategy in enumerate(strategies, start=1):
            try:
                result = strategy(response_text)
                if result is not None:
                    print(f"   • Fallback strategy {index} succeeded")
                    return result
            except Exception as exc:  # noqa: BLE001 - debugging aid
                print(f"   • Fallback strategy {index} failed: {exc}")
        return None

    @staticmethod
    def _clean_json_response(response: str) -> str:
        if not response:
            return ""

        cleaned = response.strip()
        patterns = (
            ("```json\n", "```"),
            ("```json", "```"),
            ("```\n", "```"),
            ("```", "```"),
        )
        for start, end in patterns:
            if cleaned.startswith(start):
                cleaned = cleaned[len(start) :]
                if cleaned.endswith(end):
                    cleaned = cleaned[: -len(end)]
                break

        cleaned = cleaned.strip()
        prefixes = ("Here is the JSON:", "Here's the evaluation:", "JSON response:")
        for prefix in prefixes:
            if cleaned.lower().startswith(prefix.lower()):
                cleaned = cleaned[len(prefix) :].strip()
        return cleaned

    @staticmethod
    def _extract_json_by_braces(response: str) -> Optional[Dict]:
        start_idx = response.find("{")
        end_idx = response.rfind("}") + 1
        if start_idx != -1 and end_idx > start_idx:
            return json.loads(response[start_idx:end_idx])
        return None

    @staticmethod
    def _aggressive_clean_and_parse(response: str) -> Optional[Dict]:
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if not match:
            return None
        json_str = match.group()
        json_str = re.sub(r"[\r\n\t]+", " ", json_str)
        json_str = re.sub(r"\s+", " ", json_str)
        return json.loads(json_str)

    @staticmethod
    def _extract_json_by_issues_pattern(response: str) -> Optional[Dict]:
        match = re.search(r"\"issues\"\s*:\s*\[.*?\]", response, re.DOTALL)
        if not match:
            return None
        return json.loads("{" + match.group() + "}")

    @staticmethod
    def _require_env(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise ValueError(f"{name} environment variable is required. Please check your .env file.")
        return value
