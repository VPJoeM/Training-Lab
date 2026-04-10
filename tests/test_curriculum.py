"""tests for the curriculum loader -- makes sure markdown, yaml, and scenarios all parse"""

import pytest
from unittest.mock import patch


def _load_with_path(curriculum_path):
    """helper to call load_curriculum with a specific path"""
    with patch("app.main.settings") as mock:
        mock.CURRICULUM_PATH = curriculum_path
        from app.main import load_curriculum
        return load_curriculum()


class TestCurriculumLoader:

    def test_loads_tracks(self, sample_curriculum):
        tracks = _load_with_path(sample_curriculum)
        assert "baremetal" in tracks
        assert tracks["baremetal"]["display_name"] == "Bare Metal H100"

    def test_loads_modules(self, sample_curriculum):
        tracks = _load_with_path(sample_curriculum)
        modules = tracks["baremetal"]["modules"]
        assert len(modules) == 2
        assert modules[0]["id"] == "01-test-module"
        assert modules[1]["id"] == "02-scenario-module"

    def test_module_numbers(self, sample_curriculum):
        tracks = _load_with_path(sample_curriculum)
        modules = tracks["baremetal"]["modules"]
        assert modules[0]["number"] == "01"
        assert modules[1]["number"] == "02"

    def test_lesson_title_from_markdown(self, sample_curriculum):
        tracks = _load_with_path(sample_curriculum)
        modules = tracks["baremetal"]["modules"]
        assert modules[0]["title"] == "Test Module"
        assert modules[1]["title"] == "Scenario Module"

    def test_lesson_html_rendered(self, sample_curriculum):
        tracks = _load_with_path(sample_curriculum)
        html = tracks["baremetal"]["modules"][0]["lesson_html"]
        assert "<h1" in html or "<h2" in html
        assert "test lesson" in html.lower()

    def test_scripts_parsed(self, sample_curriculum):
        tracks = _load_with_path(sample_curriculum)
        scripts = tracks["baremetal"]["modules"][0]["scripts"]
        assert len(scripts) == 1
        assert scripts[0]["name"] == "test-script.sh"

    def test_scenarios_loaded(self, sample_curriculum):
        tracks = _load_with_path(sample_curriculum)
        scenarios = tracks["baremetal"]["modules"][1]["scenarios"]
        assert len(scenarios) == 1

        sc = scenarios[0]
        assert sc["id"] == "fix-the-thing"
        assert sc["title"] == "Fix The Thing"
        assert sc["difficulty"] == "Easy"
        assert len(sc["hints"]) == 2

    def test_scenario_has_path(self, sample_curriculum):
        tracks = _load_with_path(sample_curriculum)
        sc = tracks["baremetal"]["modules"][1]["scenarios"][0]
        assert "fix-the-thing" in sc["path"]

    def test_missing_curriculum_dir(self, tmp_path):
        tracks = _load_with_path(str(tmp_path / "nonexistent"))
        assert tracks == {}

    def test_empty_track_dir(self, tmp_path):
        track = tmp_path / "track-empty"
        track.mkdir()
        tracks = _load_with_path(str(tmp_path))
        assert "empty" in tracks
        assert tracks["empty"]["modules"] == []

    def test_module_without_lesson(self, tmp_path):
        """module dir exists but no lesson.md -- should still load with empty content"""
        track = tmp_path / "track-baremetal"
        track.mkdir()
        m = track / "01-no-lesson"
        m.mkdir()

        tracks = _load_with_path(str(tmp_path))
        modules = tracks["baremetal"]["modules"]
        assert len(modules) == 1
        assert modules[0]["lesson_html"] == ""
        assert modules[0]["title"] == "No Lesson"
