#!/usr/bin/env python3
"""Command-line orchestrator for the quiz localization workflow."""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from dotenv import load_dotenv

from toolkit import (
    SUPPORTED_LANGUAGES,
    DirectoryCleaner,
    QuizConverter,
    QuizEvaluator,
    serve_dashboard,
)

load_dotenv()

CLEAN_TARGETS = {
    "clean_generated_quizzes": ("Generated Quizzes", "clean_generated_quizzes"),
    "clean_markdown_quizzes": ("Markdown Quizzes", "clean_markdown_quizzes"),
    "clean_eval_results": ("Evaluation Results", "clean_eval_results"),
}


CONCISE_HELP = """Localization Tool

Usage:   python app.py [COMMAND] [OPTIONS]

Commands:
  --convert-<lang>                        Convert <lang> JSONL quizzes to markdown
  --convert-all                           Convert all supported languages
  --eval-<lang>                           Evaluate <lang> markdown quizzes
  --eval-all                              Evaluate all supported languages
  --clean-generated-quizzes-<lang|all>    Clean generated quizzes directory
  --clean-markdown-quizzes-<lang|all>     Clean markdown quizzes directory
  --clean-eval-results-<lang|all>         Clean evaluation results directory
  --dashboard                             Serve dashboard.html locally (port 8083)

Supported languages: english, spanish, polish, french, russian, german, portuguese, japanese, serbian, arabic, hebrew

Options:
  --label <str>                           Required version label for evaluation commands
  -h, --help                              Show this help message and exit

Examples:
  python app.py --convert-english
  python app.py --eval-spanish --label test
  python app.py --clean-markdown-quizzes-all
  python app.py --dashboard
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--label")
    operation_group = parser.add_mutually_exclusive_group(required=True)

    _add_language_flags(operation_group, "convert")
    _add_language_flags(operation_group, "eval")

    for target in CLEAN_TARGETS:
        _add_language_flags(operation_group, target)

    operation_group.add_argument("--dashboard", action="store_true")

    return parser


def _add_language_flags(group: argparse._MutuallyExclusiveGroup, prefix: str) -> None:
    flag_prefix = prefix.replace("_", "-")
    group.add_argument(
        f"--{flag_prefix}-all",
        action="store_true",
        dest=f"{prefix}_all",
    )
    for language in SUPPORTED_LANGUAGES:
        group.add_argument(
            f"--{flag_prefix}-{language}",
            action="store_true",
            dest=f"{prefix}_{language}",
        )


def main(argv: Optional[list[str]] = None) -> int:
    provided_args = list(argv) if argv is not None else sys.argv[1:]
    if any(arg in ("-h", "--help") for arg in provided_args):
        print(CONCISE_HELP)
        return 0

    parser = build_parser()
    args = parser.parse_args(provided_args)

    operation, payload = _resolve_operation(args)
    label_value = args.label.strip() if isinstance(args.label, str) else ""

    if operation in {"eval", "eval_all"} and not label_value:
        print("❌ The --label option is required when running evaluation commands.")
        return 1

    if operation == "convert":
        return _run_convert(payload)  # type: ignore[arg-type]
    if operation == "convert_all":
        return _run_convert_all()
    if operation == "eval":
        return _run_eval(payload, label_value)  # type: ignore[arg-type]
    if operation == "eval_all":
        return _run_eval_all(label_value)
    if operation in CLEAN_TARGETS:
        return _run_clean(operation, payload)  # type: ignore[arg-type]
    if operation == "serve_dashboard":
        return _run_serve_dashboard()

    print("❌ No operation specified")
    return 1


def _resolve_operation(args: argparse.Namespace) -> tuple[str, Optional[object]]:
    for language in SUPPORTED_LANGUAGES:
        if getattr(args, f"convert_{language}"):
            return "convert", language
    if args.convert_all:
        return "convert_all", None

    for language in SUPPORTED_LANGUAGES:
        if getattr(args, f"eval_{language}"):
            return "eval", language
    if args.eval_all:
        return "eval_all", None

    for target in CLEAN_TARGETS:
        if getattr(args, f"{target}_all"):
            return target, None
        for language in SUPPORTED_LANGUAGES:
            if getattr(args, f"{target}_{language}"):
                return target, language

    if args.dashboard:
        return "serve_dashboard", None

    return "", None


def _run_convert(language: str) -> int:
    converter = QuizConverter()
    print(f"🚀 Starting conversion for {language.title()} quizzes...")
    return 0 if converter.convert_language(language) else 1


def _run_convert_all() -> int:
    converter = QuizConverter()
    print("🌍 Starting conversion for ALL supported languages...")
    return 0 if converter.convert_all_languages() else 1


def _run_eval(language: str, label: str) -> int:
    evaluator = QuizEvaluator()
    print(f"🤖 Starting AI evaluation for {language.title()} content...")
    return 0 if evaluator.evaluate_language(language, label) else 1


def _run_eval_all(label: str) -> int:
    evaluator = QuizEvaluator()
    print("🌍 Starting AI evaluation for ALL supported languages...")
    return 0 if evaluator.evaluate_all_languages(label) else 1


def _run_clean(target: str, language: Optional[str]) -> int:
    target_label, method_name = CLEAN_TARGETS[target]
    cleaner = DirectoryCleaner()
    method = getattr(cleaner, method_name)

    if language:
        print(f"🧹 Cleaning {language.title()} {target_label}...")
        success = method(language)
    else:
        print(f"🧹 Cleaning ALL {target_label}...")
        success = method()

    if success and target == "clean_eval_results":
        QuizEvaluator().refresh_file_index()

    return 0 if success else 1


def _run_serve_dashboard() -> int:
    try:
        serve_dashboard()
    except FileNotFoundError as exc:
        print(f"❌ {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
