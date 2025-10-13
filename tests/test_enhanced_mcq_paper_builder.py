"""Tests for enhanced MCQ paper builder helpers."""

from pathlib import Path
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


import enhanced_mcq_paper_builder as builder  # noqa: E402
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


def test_generate_sets_falls_back_to_default_config(tmp_path, monkeypatch):
    sections = [_sample_section()]

    captured_configs = []

    class DummyGenerator:
        def __init__(self, *_, config=None, **__):
            captured_configs.append(config)

        def set_set_name(self, name):
            self.set_name = name

        def add_page(self):
            pass

        def generate_from_sections(self, sections):
            return sum(section.marks_per_question for section in sections)

        def output(self, _path):
            pass

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(builder, 'EnhancedMCQPaperGenerator', DummyGenerator)
    monkeypatch.setattr(builder, 'rearrange_for_booklet', lambda *args, **kwargs: None)
    monkeypatch.setattr(builder, 'create_a3_booklet_pdf', lambda *args, **kwargs: None)

    result = generate_enhanced_mcq_sets_with_keys(
        sections_data=sections,
        num_sets=1,
        config=None,
        no_shuffle=True
    )

    assert "Set A" in result
    assert captured_configs
    assert captured_configs[0].title == "Standard High School"
