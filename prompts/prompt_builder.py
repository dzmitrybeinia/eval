#!/usr/bin/env python3
"""Prompt builder utility for quiz evaluation workflows."""

from pathlib import Path
from typing import Dict


class PromptBuilder:
    """Load and assemble prompts for different evaluation strategies."""

    def __init__(self, prompts_dir: str = "prompts") -> None:
        self.prompts_dir = Path(prompts_dir)
        self.base_prompt_path = self.prompts_dir / "base_prompt.md"
        self.languages_dir = self.prompts_dir / "languages"
        self.combined_expert_path = self.prompts_dir / "combined_expert.md"
        self.distractor_expert_path = self.prompts_dir / "distractor_expert.md"

    def build_prompt(self, language: str, content: str, step: str = "single") -> str:
        """Return the prompt for the requested evaluation step."""
        language_name = self._language_name(language)

        if step == "distractors":
            return self._build_distractors_prompt(language_name, content)

        if step == "combined" or language.lower() != "english":
            return self._build_combined_prompt(language_name, content)

        return self._build_single_step_prompt(language_name, content)

    def _build_single_step_prompt(self, language_name: str, content: str) -> str:
        try:
            base_prompt = self.base_prompt_path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:  # pragma: no cover - environment issue
            raise FileNotFoundError(f"Base prompt not found: {self.base_prompt_path}") from exc

        language_prompt = self._load_language_prompt(language_name)
        base_prompt = base_prompt.replace("{LANGUAGE_NAME}", language_name)

        return (
            f"{base_prompt}\n\n---\n\n{language_prompt}\n\n---\n\n"
            f"## CONTENT FOR EVALUATION\n\n{content}\n\n"
            "Remember: Focus only on identifying actual issues. Return only valid JSON without any additional text."
        )

    def _build_combined_prompt(self, language_name: str, content: str) -> str:
        try:
            combined_prompt = self.combined_expert_path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:  # pragma: no cover - environment issue
            raise FileNotFoundError(
                f"Combined expert prompt not found: {self.combined_expert_path}"
            ) from exc

        language_prompt = self._load_language_prompt(language_name)
        combined_prompt = combined_prompt.replace("{LANGUAGE_NAME}", language_name)

        return (
            f"{combined_prompt}\n\n---\n\n{language_prompt}\n\n---\n\n"
            f"## CONTENT FOR EVALUATION\n\n{content}\n\n"
            "Remember: Apply both linguistic and localization expertise with language-specific knowledge. "
            "Follow deduplication rules strictly. Return only valid JSON without any additional text."
        )

    def _build_distractors_prompt(self, language_name: str, content: str) -> str:
        try:
            distractors_prompt = self.distractor_expert_path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:  # pragma: no cover - environment issue
            raise FileNotFoundError(
                f"Distractor expert prompt not found: {self.distractor_expert_path}"
            ) from exc

        language_prompt = self._load_language_prompt(language_name)
        distractors_prompt = distractors_prompt.replace("{LANGUAGE_NAME}", language_name)

        return (
            f"{distractors_prompt}\n\n---\n\n{language_prompt}\n\n---\n\n"
            f"## CONTENT FOR EVALUATION\n\n{content}\n\n"
            "Focus ONLY on identifying clear, obvious problems with distractors. Be conservative - only report issues "
            "you're confident about. Don't suggest improvements unless there's an obvious fix. Return only valid JSON "
            "without any additional text."
        )

    def _load_language_prompt(self, language_name: str) -> str:
        language_code = language_name.lower()
        language_prompt_path = self.languages_dir / f"{language_code}.md"
        try:
            return language_prompt_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return (
                f"## LANGUAGE FOCUS: {language_name}\n\n"
                f"Focus on {language_name} linguistic accuracy and localization quality."
            )

    @staticmethod
    def _language_name(language: str) -> str:
        mapping = {
            "english": "English",
            "spanish": "Spanish",
            "polish": "Polish",
            "russian": "Russian",
            "serbian": "Serbian",
            "japanese": "Japanese",
            "french": "French",
            "german": "German",
            "portuguese": "Portuguese",
        }
        return mapping.get(language.lower(), language.title())

    def get_available_languages(self) -> Dict[str, str]:
        """Return the languages that have dedicated markdown prompts."""
        languages: Dict[str, str] = {}
        for file_path in self.languages_dir.glob("*.md"):
            language_code = file_path.stem
            try:
                first_line = file_path.read_text(encoding="utf-8").splitlines()[0]
            except (OSError, IndexError):
                languages[language_code] = language_code.title()
                continue

            if "LANGUAGE FOCUS:" in first_line:
                language_name = first_line.split("LANGUAGE FOCUS:")[1].split("(")[0].strip()
                languages[language_code] = language_name
            else:
                languages[language_code] = language_code.title()
        return languages


def main() -> None:
    """Quick manual test for developers."""
    builder = PromptBuilder()

    languages = builder.get_available_languages()
    print("Available languages:")
    for code, name in sorted(languages.items()):
        print(f"  {code}: {name}")

    if "polish" in languages:
        sample = "# Test Content\nThis is a test content for evaluation."
        prompt = builder.build_prompt("polish", sample, step="combined")
        print(f"\nGenerated prompt length: {len(prompt)} characters")
        print("Prompt preview (first 300 chars):")
        print(prompt[:300] + "...")


if __name__ == "__main__":
    main()
