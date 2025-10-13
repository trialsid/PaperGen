"""Tests for enhanced MCQ paper builder helpers."""

from pathlib import Path
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


from enhanced_mcq_paper_builder import generate_enhanced_mcq_sets_with_keys  # noqa: E402


def _sample_section():
    return {
        "name": "Sample Section",
        "description": "Demo description",
        "questions": [
            {
                "question_text": "Sample question?",
                "choices": ["A", "B", "C", "D"],
                "answer": "A",
            }
        ],
    }


def test_generate_sets_rejects_more_than_26_sets():
    sections = [_sample_section()]

    with pytest.raises(ValueError) as excinfo:
        generate_enhanced_mcq_sets_with_keys(sections_data=sections, num_sets=27)

    assert "exceeds the supported maximum" in str(excinfo.value)


def test_generate_sets_rejects_non_positive_set_count():
    sections = [_sample_section()]

    with pytest.raises(ValueError) as excinfo:
        generate_enhanced_mcq_sets_with_keys(sections_data=sections, num_sets=0)

    assert "at least 1" in str(excinfo.value)