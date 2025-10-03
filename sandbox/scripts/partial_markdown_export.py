#!/usr/bin/env python3
"""Export partial quiz markdown slices for LLM or SLM evaluation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toolkit.constants import SUPPORTED_LANGUAGES


def parse_args() -> argparse.Namespace:
    """Build and return the CLI arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Convert generated quiz JSON files into markdown snippets that capture "
            "only the sections created by either the LLM (Intro/Content slides) or "
            "the SLM (interactive questions)."
        )
    )
    parser.add_argument(
        "-l",
        "--language",
        action="append",
        choices=SUPPORTED_LANGUAGES,
        help="Language(s) to process. Defaults to all supported languages.",
    )
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Export only the LLM produced sections (Intro and Content slides).",
    )
    parser.add_argument(
        "--slm",
        action="store_true",
        help="Export only the SLM produced sections (Statement, Answer, Feedback).",
    )
    parser.add_argument(
        "--base-dir",
        default=None,
        help=(
            "Base directory for resolving paths. Defaults to the repository root "
            "(two levels above this script)."
        ),
    )
    parser.add_argument(
        "--input-root",
        default="generated_quizzes",
        help="Directory that stores the generated quiz JSON files.",
    )
    parser.add_argument(
        "--output-root",
        default="sandbox",
        help="Directory where markdown exports should be written.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing markdown files instead of skipping them.",
    )
    return parser.parse_args()


def determine_base_dir(explicit: str | None) -> Path:
    """Resolve the base directory, defaulting to the repository root."""
    if explicit:
        return Path(explicit).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def resolve_dir(base_dir: Path, relative_or_absolute: str) -> Path:
    """Resolve a directory allowing both relative and absolute inputs."""
    candidate = Path(relative_or_absolute).expanduser()
    if candidate.is_absolute():
        return candidate
    return (base_dir / candidate).resolve()


def load_quiz(json_path: Path) -> Dict:
    """Load a quiz JSONL file into memory."""
    with json_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def select_languages(requested: Sequence[str] | None) -> Iterable[str]:
    """Return the languages to process in CLI order."""
    if requested:
        seen: set[str] = set()
        for language in requested:
            if language not in seen:
                seen.add(language)
                yield language
        return
    for language in SUPPORTED_LANGUAGES:
        yield language


def lesson_name(json_file: Path, data: Dict) -> str:
    """Derive the lesson name following converter.py heuristics."""
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


def build_llm_section(data: Dict) -> List[str]:
    """Build markdown lines for the LLM generated sections."""
    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        return []

    output: List[str] = []
    for index, section in enumerate(sections):
        if not isinstance(section, dict):  # defensive guard
            continue

        heading = "## Intro" if index == 0 else "## Content slide"
        title = section.get("title")
        content = section.get("content")
        themes = section.get("themes", [])

        output.append(heading)
        output.append("")

        if title:
            output.append(f"### {title}")
            output.append("")

        if content:
            output.append(content)
            output.append("")

        if themes:
            output.append("#### **Themes:**")
            for theme in themes:
                output.append(f"- {theme}")
            output.append("")

    return output


def build_slm_section(data: Dict) -> List[str]:
    """Build markdown lines for the SLM generated questions."""
    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        return []

    output: List[str] = []

    for slide_index, slide in enumerate(slides):
        if not isinstance(slide, dict) or slide.get("status") != "Success":
            continue

        objects = slide.get("generatedObjects", [])
        if not isinstance(objects, list):
            continue

        for obj in objects:
            if not isinstance(obj, dict) or obj.get("status") != "Success":
                continue

            obj_type = obj.get("type")
            content = obj.get("generatedContent", {})
            if not isinstance(content, dict):
                continue

            if obj_type == "YesNo":
                append_yes_no(output, content)
            elif obj_type == "DynamicQuiz":
                append_multiple_choice(output, content)
            elif obj_type == "Match":
                append_match(output, content)
            elif obj_type == "FillInTheBlanks":
                append_fill_in_the_blanks(output, content)
            elif obj_type == "KahootQuiz":
                append_kahoot(output, content)

    return output


def append_yes_no(target: List[str], content: Dict) -> None:
    statement = content.get("statement", "")
    answer_flag = content.get("isStatementTrue")
    feedback = content.get("feedback") or content.get("explanation", "")

    target.append("## YesNo")
    target.append("")
    target.append(f"**Statement:** {statement}")
    target.append("")
    if answer_flag is not None:
        target.append(f"**Answer:** {'True' if answer_flag else 'False'}")
        target.append("")
    if feedback:
        target.append("**Feedback:**")
        target.append(feedback)
        target.append("")
    target.append("")


def append_multiple_choice(target: List[str], content: Dict) -> None:
    question = content.get("question", "")
    answers = content.get("answers", [])
    feedback = content.get("feedback") or content.get("explanation", "")

    target.append("## Multiple Choice")
    target.append("")
    target.append(f"**Question:** {question}")
    target.append("")
    target.append("**Options:**")

    correct_answer = None
    if isinstance(answers, list):
        for answer in answers:
            if not isinstance(answer, dict):
                continue
            answer_text = answer.get("answer", "")
            marker = "[x]" if answer.get("correct", False) else "[ ]"
            target.append(f"{marker} {answer_text}")
            if marker == "[x]":
                correct_answer = answer_text

    target.append("")
    if correct_answer:
        target.append(f"**Correct Answer:** {correct_answer}")
        target.append("")

    if feedback:
        target.append("**Explanation:**")
        target.append(feedback)
        target.append("")
    target.append("")


def append_match(target: List[str], content: Dict) -> None:
    pairs = content.get("pairs", [])
    feedback = content.get("feedback") or content.get("explanation", "")

    target.append("## Match")
    target.append("")
    if isinstance(pairs, list):
        for left_right in pairs:
            if not isinstance(left_right, dict):
                continue
            left = left_right.get("left", "")
            right = left_right.get("right", "")
            target.append(f"- {left} -> {right}")
    target.append("")

    if feedback:
        target.append("**Feedback:**")
        target.append(feedback)
        target.append("")
    target.append("")


def append_fill_in_the_blanks(target: List[str], content: Dict) -> None:
    prompt = content.get("prompt", "")
    blanks = content.get("blanks", [])
    feedback = content.get("feedback") or content.get("explanation", "")

    target.append("## Fill In The Blanks")
    target.append("")
    target.append(prompt)
    target.append("")

    if isinstance(blanks, list):
        target.append("**Answers:**")
        for blank in blanks:
            target.append(f"- {blank}")
        target.append("")

    if feedback:
        target.append("**Feedback:**")
        target.append(feedback)
        target.append("")
    target.append("")


def append_kahoot(target: List[str], content: Dict) -> None:
    question = content.get("question", "")
    answers = content.get("answers", [])
    feedback = content.get("feedback") or content.get("explanation", "")

    target.append("## Kahoot Quiz")
    target.append("")
    target.append(f"**Question:** {question}")
    target.append("")

    if isinstance(answers, list):
        target.append("**Options:**")
        for answer in answers:
            if not isinstance(answer, dict):
                continue
            answer_text = answer.get("answer", "")
            marker = "[x]" if answer.get("correct", False) else "[ ]"
            target.append(f"{marker} {answer_text}")
        target.append("")

    if feedback:
        target.append("**Feedback:**")
        target.append(feedback)
        target.append("")
    target.append("")


def export_quiz(
    quiz_path: Path,
    data: Dict,
    output_dir: Path,
    include_llm: bool,
    include_slm: bool,
    overwrite: bool,
) -> bool:
    """Write the markdown export for a single quiz file."""
    lesson = lesson_name(quiz_path, data)
    lines: List[str] = [f"# Lesson name: {lesson}", ""]

    if include_llm:
        llm_lines = build_llm_section(data)
        if not llm_lines:
            print(f"   Warning: No LLM sections found in {quiz_path.name}; skipping LLM export")
        else:
            lines.extend(llm_lines)

    if include_slm:
        slm_lines = build_slm_section(data)
        if not slm_lines:
            print(f"   Warning: No SLM sections found in {quiz_path.name}; skipping SLM export")
        else:
            lines.extend(slm_lines)

    # If we only added the heading, there is nothing to write.
    if len(lines) <= 2:
        return False

    suffix = ".llm" if include_llm and not include_slm else ""
    if include_slm and not include_llm:
        suffix = ".slm"
    output_path = output_dir / f"{quiz_path.stem}{suffix}.md"

    if output_path.exists() and not overwrite:
        print(f"   Skipping existing file: {output_path.name}")
        return False

    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines).rstrip() + "\n"
    output_path.write_text(text, encoding="utf-8")
    print(f"   Wrote {output_path.name}")
    return True


def main() -> None:
    args = parse_args()

    if args.llm == args.slm:
        raise SystemExit("Select exactly one mode: use --llm or --slm.")

    base_dir = determine_base_dir(args.base_dir)
    input_root = resolve_dir(base_dir, args.input_root)
    output_root = resolve_dir(base_dir, args.output_root)

    mode_label = "LLM" if args.llm else "SLM"
    print(f"Starting {mode_label} markdown export")
    print(f"Input directory: {input_root}")
    print(f"Output directory: {output_root}")
    print("=" * 60)

    total_written = 0
    for language in select_languages(args.language):
        language_input = input_root / language
        language_output = output_root / language

        if not language_input.exists():
            print(f"Skipping {language} (missing directory {language_input})")
            continue

        json_files = sorted(language_input.glob("*.jsonl"))
        if not json_files:
            print(f"Skipping {language} (no .jsonl files found)")
            continue

        print(f"\nProcessing language: {language}")
        for quiz_path in json_files:
            try:
                data = load_quiz(quiz_path)
            except json.JSONDecodeError as exc:
                print(f"   Error: Failed to parse {quiz_path.name}: {exc}")
                continue

            if export_quiz(
                quiz_path,
                data,
                language_output,
                include_llm=args.llm,
                include_slm=args.slm,
                overwrite=args.overwrite,
            ):
                total_written += 1

    print("\n" + "=" * 60)
    print(f"Summary: Export complete. Files written: {total_written}")


if __name__ == "__main__":
    main()
