"""Directory maintenance utilities."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Iterable

from .constants import SUPPORTED_LANGUAGES


class DirectoryCleaner:
    """Clean generated, markdown, and evaluation directories."""

    def __init__(self, base_dir: Path | str = ".") -> None:
        base_path = Path(base_dir)
        self.generated_quizzes_dir = base_path / "generated_quizzes"
        self.markdown_quizzes_dir = base_path / "markdown_quizzes"
        self.eval_results_dir = base_path / "eval_results"
        self.issues_dir = base_path / "issues"

    def clean_generated_quizzes(self, language: str | None = None) -> bool:
        return self._clean(self.generated_quizzes_dir, language, "Generated Quizzes")

    def clean_markdown_quizzes(self, language: str | None = None) -> bool:
        return self._clean(self.markdown_quizzes_dir, language, "Markdown Quizzes")

    def clean_eval_results(self, language: str | None = None) -> bool:
        return self._clean(self.eval_results_dir, language, "Evaluation Results")

    def clean_issues(self, language: str | None = None) -> bool:
        return self._clean(self.issues_dir, language, "Issues")

    def _clean(self, base_path: Path, language: str | None, label: str) -> bool:
        if language:
            return self._clean_language(base_path, language, label)
        return self._clean_all(base_path, label)

    def _clean_language(self, base_path: Path, language: str, label: str) -> bool:
        target_dir = base_path / language
        if not target_dir.exists():
            print(f"⏭️  Directory not found: {target_dir}")
            print(f"📝 Nothing to clean for {language.title()} {label.lower()}")
            return True

        if self._is_empty(target_dir.iterdir()):
            print(f"📭 Directory is already empty: {target_dir}")
            return True

        print(f"🧹 Cleaning {language.title()} {label}...")
        return self._remove_contents(target_dir, language_title=language.title(), label=label)

    def _clean_all(self, base_path: Path, label: str) -> bool:
        if not base_path.exists():
            print(f"⏭️  Directory not found: {base_path}")
            print(f"📝 Nothing to clean for {label.lower()}")
            return True

        if self._is_empty(base_path.iterdir()):
            print(f"📭 Directory is already empty: {base_path}")
            return True

        languages = [d.name.title() for d in base_path.iterdir() if d.is_dir() and d.name in SUPPORTED_LANGUAGES]
        if languages:
            print(f"🌍 Language directories: {', '.join(languages)}")

        print(f"🧹 Cleaning ALL {label}...")
        return self._remove_contents(base_path, language_title=None, label=label)

    def _remove_contents(self, path: Path, *, language_title: str | None, label: str) -> bool:
        files = list(path.rglob("*"))
        file_count = len([entry for entry in files if entry.is_file()])
        dir_count = len([entry for entry in files if entry.is_dir()])
        print(f"📊 Found: {file_count} files, {dir_count} subdirectories")

        try:
            for item in path.iterdir():
                if item.is_file():
                    item.unlink()
                else:
                    shutil.rmtree(item)

            scope = f"{language_title} {label.lower()}" if language_title else f"ALL {label.lower()}"
            print(f"✅ Successfully cleaned {scope}")
            print(f"📝 Removed {file_count} files and {dir_count} subdirectories")
            return True
        except Exception as exc:  # noqa: BLE001 - user needs to see cleanup issues
            scope = f"{language_title} {label.lower()}" if language_title else f"ALL {label.lower()}"
            print(f"❌ Error cleaning {scope}: {exc}")
            return False

    @staticmethod
    def _is_empty(entries: Iterable[Path]) -> bool:
        return not any(True for _ in entries)
