"""Quiz conversion utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .constants import SUPPORTED_LANGUAGES


class QuizConverter:
    """Convert generated quiz JSON files into markdown."""

    def __init__(self, base_dir: Path | str = ".") -> None:
        base_path = Path(base_dir)
        self.quizzes_dir = base_path / "generated_quizzes"
        self.output_dir = base_path / "markdown_quizzes"

    def convert_language(self, language: str) -> bool:
        """Convert all JSON files for a specific language."""
        source_dir = self.quizzes_dir / language
        target_dir = self.output_dir / language

        if not source_dir.exists():
            print(f"❌ Source directory not found: {source_dir}")
            return False

        target_dir.mkdir(parents=True, exist_ok=True)
        json_files = sorted(source_dir.glob("*.jsonl"))

        if not json_files:
            print(f"❌ No JSONL files found in {source_dir}")
            return False

        converted = 0
        skipped = 0

        for json_file in json_files:
            output_file = target_dir / f"{json_file.stem}.md"
            if output_file.exists():
                print(f"⏭️  Skipping {json_file.name} (output already exists)")
                skipped += 1
                continue

            try:
                print(f"🔄 Converting {json_file.name}...")
                if self._convert_file(json_file, output_file):
                    converted += 1
                    print(f"✅ Created {output_file.name}")
                else:
                    print(f"❌ Failed to convert {json_file.name}")
            except Exception as exc:  # noqa: BLE001 - we want to surface conversion issues
                print(f"❌ Error converting {json_file.name}: {exc}")

        print("\n📊 Conversion Summary:")
        print(f"   ✅ Converted: {converted}")
        print(f"   ⏭️  Skipped: {skipped}")
        print(f"   📝 Total files: {len(json_files)}")

        return converted > 0

    def convert_all_languages(self) -> bool:
        """Convert quizzes for every supported language."""
        print("🌍 Starting conversion for ALL supported languages")
        print(f"📋 Languages to process: {', '.join(lang.title() for lang in SUPPORTED_LANGUAGES)}")
        print("=" * 60)

        successful = []
        failed = []
        skipped = []
        total_files = 0

        for language in SUPPORTED_LANGUAGES:
            print(f"\n🔄 Processing language: {language.title()}")
            print("-" * 40)

            source_dir = self.quizzes_dir / language
            if not source_dir.exists():
                print(f"⏭️  Skipping {language.title()} - no generated_quizzes directory found")
                skipped.append(language)
                continue

            json_files = list(source_dir.glob("*.jsonl"))
            if not json_files:
                print(f"⏭️  Skipping {language.title()} - no JSONL files found")
                skipped.append(language)
                continue

            if self.convert_language(language):
                successful.append(language)
                total_files += len(json_files)
            else:
                failed.append(language)

        print("\n" + "=" * 60)
        print("🎯 CONVERSION CYCLE COMPLETE")
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

        print(f"\n📊 Total files converted: {total_files}")
        return bool(successful)

    def _convert_file(self, json_file: Path, output_file: Path) -> bool:
        try:
            with open(json_file, "r", encoding="utf-8") as handle:
                data = json.load(handle)

            lesson_name = self._lesson_name(json_file, data)
            markdown = self._build_markdown(data, lesson_name)

            with open(output_file, "w", encoding="utf-8") as handle:
                handle.write(markdown)
            return True
        except Exception as exc:  # noqa: BLE001 - conversion should never hide exceptions
            print(f"Error processing {json_file}: {exc}")
            return False

    def _lesson_name(self, json_file: Path, data: Dict) -> str:
        if isinstance(data, dict):
            metadata = data.get("fileMetadata", {})
            if isinstance(metadata, dict) and metadata.get("sourceFilePath"):
                return metadata["sourceFilePath"]

            sections = data.get("sections")
            if isinstance(sections, list) and sections:
                title = sections[0].get("title")
                if title:
                    return title

        filename = json_file.stem
        if "__" in filename:
            return filename.split("__", maxsplit=1)[0].replace("_", " ").title()
        return filename.replace("_", " ").title()

    def _build_markdown(self, data: Dict, lesson_name: str) -> str:
        md_lines: List[str] = [f"# Lesson name: {lesson_name}", ""]
        sections = data.get("sections", []) if isinstance(data, dict) else []
        slides = data.get("slides", []) if isinstance(data, dict) else []

        if slides:
            self._slides_to_markdown(slides, md_lines, sections)
        elif sections:
            self._sections_to_markdown(sections, md_lines)
        elif isinstance(data, dict) and any(key in data for key in ("generatedObjects", "content", "questions")):
            md_lines.append("## Content")
            md_lines.append("")
            md_lines.append("### Quiz Content")
            md_lines.append("")
            if data.get("content"):
                md_lines.append(str(data["content"]))
                md_lines.append("")

        return "\n".join(md_lines)

    def _slides_to_markdown(self, slides: List[Dict], md_lines: List[str], sections: List[Dict] | None) -> None:
        intro_added = False
        slide_index = 0

        for slide_num, slide in enumerate(slides):
            if slide.get("status") != "Success":
                continue

            for obj in slide.get("generatedObjects", []):
                if obj.get("status") != "Success":
                    continue

                obj_type = obj.get("type", "")
                content = obj.get("generatedContent", {})
                inputs = obj.get("inputs", {})

                if not intro_added and slide_num == 0:
                    self._add_intro(md_lines, inputs.get("factoid", "Introduction"), sections)
                    intro_added = True

                if obj_type in {"YesNo", "DynamicQuiz", "Match", "FillInTheBlanks", "KahootQuiz"}:
                    if slide_index == 0 or obj is slide.get("generatedObjects", [None])[0]:
                        self._add_content_slide(md_lines, inputs.get("factoid", f"Content {slide_num + 1}"), slide_index, sections)
                        slide_index += 1

                if obj_type == "YesNo":
                    self._add_yes_no(md_lines, content)
                elif obj_type == "DynamicQuiz":
                    self._add_multiple_choice(md_lines, content)
                elif obj_type == "Match":
                    self._add_match(md_lines, content)
                elif obj_type == "FillInTheBlanks":
                    self._add_fill_blanks(md_lines, content)
                elif obj_type == "KahootQuiz":
                    self._add_kahoot(md_lines, content)

                if obj.get("status") == "Failure" or obj.get("error"):
                    md_lines.append(f"<!-- Error processing slide {slide_num}: {obj.get('error', 'Unknown error')} -->")
                    md_lines.append("")

    def _sections_to_markdown(self, sections: List[Dict], md_lines: List[str]) -> None:
        for index, section in enumerate(sections):
            title = section.get("title", f"Section {index + 1}")
            content = section.get("content", "")
            themes = section.get("themes", [])

            if index == 0:
                md_lines.append("## Intro")
            else:
                md_lines.append("## Content slide")
            md_lines.append("")
            md_lines.append(f"### {title}")
            md_lines.append("")
            if content:
                md_lines.append(content)
                md_lines.append("")
            if themes:
                md_lines.append("#### **Themes:**")
                for theme in themes:
                    md_lines.append(f"- {theme}")
                md_lines.append("")

    def _add_intro(self, md_lines: List[str], factoid: str, sections: List[Dict] | None) -> None:
        if not sections:
            return
        section = sections[0]

        md_lines.append("## Intro")
        md_lines.append("")
        md_lines.append(f"### {section.get('title', factoid.title())}")
        md_lines.append("")

        content = section.get("content", "")
        if content:
            md_lines.append(content)
            md_lines.append("")

        themes = section.get("themes", [])
        if themes:
            md_lines.append("#### **Themes:**")
            for theme in themes:
                md_lines.append(f"- {theme}")
            md_lines.append("")

    def _add_content_slide(self, md_lines: List[str], factoid: str, slide_index: int, sections: List[Dict] | None) -> None:
        if not sections or len(sections) <= slide_index + 1:
            return
        section = sections[slide_index + 1]

        md_lines.append("## Content slide")
        md_lines.append("")
        md_lines.append(f"### {section.get('title', factoid.title())}")
        md_lines.append("")

        content = section.get("content", "")
        if content:
            md_lines.append(content)
            md_lines.append("")

        themes = section.get("themes", [])
        if themes:
            md_lines.append("#### **Themes:**")
            for theme in themes:
                md_lines.append(f"- {theme}")
            md_lines.append("")

    def _add_yes_no(self, md_lines: List[str], content: Dict) -> None:
        statement = content.get("statement", "")
        is_true = content.get("isStatementTrue", True)
        feedback = content.get("feedback", content.get("explanation", ""))

        md_lines.append("## YesNo")
        md_lines.append("")
        md_lines.append(f"**Statement:** {statement}")
        md_lines.append("")
        md_lines.append(f"**Answer:** {'True' if is_true else 'False'}")
        md_lines.append("")
        if feedback:
            md_lines.append("**Feedback:**")
            md_lines.append(feedback)
            md_lines.append("")
        md_lines.append("")

    def _add_multiple_choice(self, md_lines: List[str], content: Dict) -> None:
        question = content.get("question", "")
        answers = content.get("answers", [])
        feedback = content.get("feedback", content.get("explanation", ""))

        md_lines.append("## Multiple Choice")
        md_lines.append("")
        md_lines.append(f"**Question:** {question}")
        md_lines.append("")
        md_lines.append("**Options:**")

        correct_answer = None
        for answer in answers:
            answer_text = answer.get("answer", "")
            marker = "✓" if answer.get("correct", False) else "○"
            md_lines.append(f"{marker} {answer_text}")
            if marker == "✓":
                correct_answer = answer_text

        md_lines.append("")
        if correct_answer:
            md_lines.append(f"**Correct Answer:** {correct_answer}")
            md_lines.append("")

        if feedback:
            md_lines.append("**Explanation:**")
            md_lines.append(feedback)
            md_lines.append("")
        md_lines.append("")

    def _add_match(self, md_lines: List[str], content: Dict) -> None:
        question = content.get("question", "Match the following:")
        pairs = content.get("pairs", {})

        md_lines.append("## Match")
        md_lines.append("")
        md_lines.append(f"**Question:** {question}")
        md_lines.append("")
        md_lines.append("**Pairs:**")

        if isinstance(pairs, dict):
            for key, value in pairs.items():
                md_lines.append(f"- **{key}:** {value}")
        elif isinstance(pairs, list):
            for pair in pairs:
                if isinstance(pair, dict):
                    term = pair.get("term1") or pair.get("key", "")
                    value = pair.get("value1") or pair.get("value", "")
                    if term and value:
                        md_lines.append(f"- **{term}:** {value}")
                else:
                    md_lines.append(f"- {pair}")
        else:
            md_lines.append(f"- {pairs}")
        md_lines.append("")

    def _add_fill_blanks(self, md_lines: List[str], content: Dict) -> None:
        question = content.get("question", "")
        sentences = content.get("sentences", [])

        md_lines.append("## Fill in the Blanks")
        md_lines.append("")
        if question:
            md_lines.append(f"**Question:** {question}")
            md_lines.append("")
        md_lines.append("**Sentences:**")
        for sentence in sentences:
            text = sentence.get("text", "")
            answer = sentence.get("answer", "")
            md_lines.append(f"- {text} — **{answer}**")
        md_lines.append("")

    def _add_kahoot(self, md_lines: List[str], content: Dict) -> None:
        question = content.get("question", "")
        answers = content.get("answers", [])

        md_lines.append("## Kahoot Quiz")
        md_lines.append("")
        md_lines.append(f"**Question:** {question}")
        md_lines.append("")
        md_lines.append("**Options:**")

        for index, answer in enumerate(answers, 1):
            answer_text = answer.get("answer", "")
            marker = "✓" if answer.get("correct", False) else f"{index}."
            md_lines.append(f"{marker} {answer_text}")
        md_lines.append("")
