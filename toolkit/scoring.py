"""Scoring helpers for evaluation output."""

from __future__ import annotations

from typing import Dict, List


class SimpleScorer:
    """Calculate weighted scores based on issue severities."""

    def __init__(self, base_score: float = 10.0) -> None:
        self.base_score = base_score
        self.severity_multipliers = {
            "HIGH": 0.3,
            "MEDIUM": 0.2,
            "MINOR": 0.1,
        }
        self.issue_order = {
            "HIGH": 3,
            "MEDIUM": 2,
            "MINOR": 1,
        }

    def calculate_score(self, issues_list: List[Dict]) -> Dict:
        if not issues_list:
            return {
                "overall_quality_score": self.base_score,
                "classification": "NATIVE",
                "total_issues": 0,
                "total_penalty": 0.0,
                "issue_breakdown": {
                    "linguistic": 0,
                    "localization": 0,
                    "distractor_quality": 0,
                },
                "penalty_breakdown": {
                    "linguistic_penalty": 0.0,
                    "localization_penalty": 0.0,
                    "distractor_quality_penalty": 0.0,
                },
            }

        penalties = {
            "linguistic": 0.0,
            "localization": 0.0,
            "distractor_quality": 0.0,
        }
        counts = {
            "linguistic": 0,
            "localization": 0,
            "distractor_quality": 0,
        }

        for issue in issues_list:
            category = issue.get("category", "linguistic")
            severity = issue.get("severity", "MEDIUM")
            if category not in penalties:
                continue

            counts[category] += 1
            penalties[category] += self.severity_multipliers.get(severity, 0.2)

        total_penalty = sum(penalties.values())
        score = max(0.0, self.base_score - total_penalty)

        return {
            "overall_quality_score": round(score, 1),
            "classification": self._classify(score),
            "total_issues": sum(counts.values()),
            "total_penalty": round(total_penalty, 1),
            "issue_breakdown": counts,
            "penalty_breakdown": {
                "linguistic_penalty": round(penalties["linguistic"], 1),
                "localization_penalty": round(penalties["localization"], 1),
                "distractor_quality_penalty": round(penalties["distractor_quality"], 1),
            },
        }

    @staticmethod
    def _classify(score: float) -> str:
        if score >= 9.0:
            return "NATIVE"
        if score >= 8.0:
            return "PROFESSIONAL"
        if score >= 7.0:
            return "ACCEPTABLE"
        if score >= 6.0:
            return "SUBSTANDARD"
        if score >= 5.0:
            return "POOR"
        return "UNACCEPTABLE"
