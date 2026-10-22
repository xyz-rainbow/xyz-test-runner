import sys
import importlib.util
from pathlib import Path
from unittest.mock import MagicMock, patch

script_path = Path(__file__).parent.parent.parent / "scripts" / "xyz-test-runner.py"
spec = importlib.util.spec_from_file_location("xyz_test_runner", script_path)
xyz = importlib.util.module_from_spec(spec)
sys.modules["xyz_test_runner"] = xyz
spec.loader.exec_module(xyz)

def test_config_defaults():
    config = xyz.TestConfig("non_existent_config_file")
    assert config.get("LANGUAGE") == "en"
    assert config.get("USE_IA") == "false"

def test_testrunner_discovery(tmp_path):
    tests_dir = tmp_path / "tests"
    cat1 = tests_dir / "cat1"
    cat1.mkdir(parents=True)
    (cat1 / "test_a.py").touch()
    (cat1 / "test_b.py").touch()

    cat2 = tests_dir / "cat2"
    cat2.mkdir(parents=True)
    (cat2 / "test_c.py").touch()

    cat_hidden = tests_dir / "_hidden"
    cat_hidden.mkdir(parents=True)
    (cat_hidden / "test_d.py").touch()

    config = xyz.TestConfig("dummy")
    config.values["TEST_DIR"] = "tests"

    with patch("xyz_test_runner.OllamaManager"):
        runner = xyz.TestRunner(str(tmp_path), config)
        runner.discover_categories_and_tests()

        assert len(runner.categories) == 2
        categories_names = [c["name"] for c in runner.categories.values()]
        assert "cat1" in categories_names
        assert "cat2" in categories_names
        assert "_hidden" not in categories_names

        cat1_data = next(c for c in runner.categories.values() if c["name"] == "cat1")
        assert cat1_data["tests"] == ["test_a.py", "test_b.py"]

def test_testrunner_selection(tmp_path):
    tests_dir = tmp_path / "tests"
    cat1 = tests_dir / "cat1"
    cat1.mkdir(parents=True)
    (cat1 / "test_motor_1.py").touch()
    (cat1 / "test_normal.py").touch()

    config = xyz.TestConfig("dummy")
    config.values["TEST_DIR"] = "tests"

    with patch("xyz_test_runner.OllamaManager"):
        runner = xyz.TestRunner(str(tmp_path), config)
        runner.discover_categories_and_tests()

        # No GPU protection
        config.values["GPU_PROTECTION"] = "false"
        runner.select_all()
        cat_key = next(k for k, v in runner.categories.items() if v["name"] == "cat1")
        assert len(runner.selected_tests[cat_key]) == 2

        # GPU protection enabled
        config.values["GPU_PROTECTION"] = "true"
        runner.select_all()
        assert len(runner.selected_tests[cat_key]) == 1
        assert "test_motor_1.py" not in runner.selected_tests[cat_key]
        assert "test_normal.py" in runner.selected_tests[cat_key]

        # Deselect all
        runner.deselect_all()
        assert runner.selected_tests.get(cat_key, []) == []

        # Toggle test
        runner.toggle_test(cat_key, "test_normal.py")
        assert "test_normal.py" in runner.selected_tests[cat_key]
        runner.toggle_test(cat_key, "test_normal.py")
        assert "test_normal.py" not in runner.selected_tests[cat_key]

def test_config_load_and_save(tmp_path):
    config_file = tmp_path / "config"
    config_file.write_text("LANGUAGE=es\nUSE_IA=true\n")

    config = xyz.TestConfig(str(config_file))
    assert config.get("LANGUAGE") == "es"
    assert config.get_bool("USE_IA") is True

    config.values["LANGUAGE"] = "en"
    config.values["NEW_KEY"] = "new_value"
    config.save()

    # Reload
    config2 = xyz.TestConfig(str(config_file))
    assert config2.get("LANGUAGE") == "en"
    assert config2.get("NEW_KEY") == "new_value"

def test_testrunner_run_test_mocked(tmp_path):
    tests_dir = tmp_path / "tests"
    cat1 = tests_dir / "cat1"
    cat1.mkdir(parents=True)
    (cat1 / "test_a.py").touch()

    config = xyz.TestConfig("dummy")
    config.values["TEST_DIR"] = "tests"

    with patch("xyz_test_runner.OllamaManager"), \
         patch("xyz_test_runner.subprocess.run") as mock_run:

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "PASSED test_a.py\nFAILED test_b.py\n"
        mock_run.return_value.stderr = ""

        runner = xyz.TestRunner(str(tmp_path), config)
        runner.discover_categories_and_tests()

        cat_key = next(k for k, v in runner.categories.items() if v["name"] == "cat1")

        result = runner.run_test(cat_key, "test_a.py", verbose=False)
        assert result["result"] == "PASS"
        assert "PASSED test_a.py" in result["individual_tests"]
        assert "FAILED test_b.py" in result["individual_tests"]

        # Test failure
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "FAILED test_a.py\n"
        mock_run.return_value.stderr = ""

        result2 = runner.run_test(cat_key, "test_a.py", verbose=False)
        assert result2["result"] == "FAIL"
        assert "FAILED test_a.py" in result2["individual_tests"]

def test_generate_report_html_mocked(tmp_path):
    tests_dir = tmp_path / "tests"
    cat1 = tests_dir / "cat1"
    cat1.mkdir(parents=True)

    config = xyz.TestConfig("dummy")
    config.values["TEST_DIR"] = "tests"
    config.values["SHOW_SIGNATURE"] = "true"

    with patch("xyz_test_runner.OllamaManager"):
        runner = xyz.TestRunner(str(tmp_path), config)
        runner.categories = {"1": {"name": "cat1", "path": "tests/cat1", "tests": ["test_a.py", "test_b.py"], "enabled": True}}
        runner.report_dir = tmp_path / "reports"
        runner.report_dir.mkdir(parents=True)

        runner.results = {
            "1/test_a.py": {
                "category": "1",
                "test": "test_a.py",
                "result": "PASS",
                "time": 0.5,
                "individual_tests": ["PASSED test_1"],
                "output": "all good"
            },
            "1/test_b.py": {
                "category": "1",
                "test": "test_b.py",
                "result": "FAIL",
                "time": 0.2,
                "individual_tests": ["FAILED test_2"],
                "output": "Traceback error"
            }
        }

        report_path = runner.generate_report_html(detail_level="full")
        content = report_path

        # content already set
        assert "<html lang=\"en\">" in content
        assert "test_a.py" in content
        assert "test_b.py" in content

def test_generate_report_csv_mocked(tmp_path):
    config = xyz.TestConfig("dummy")

    with patch("xyz_test_runner.OllamaManager"):
        runner = xyz.TestRunner(str(tmp_path), config)
        runner.categories = {"1": {"name": "cat1", "path": "tests/cat1", "tests": ["test_a.py"], "enabled": True}}
        runner.report_dir = tmp_path / "reports"
        runner.report_dir.mkdir(parents=True)

        runner.results = {
            "1/test_a.py": {
                "category": "1",
                "test": "test_a.py",
                "result": "PASS",
                "time": 0.5,
            }
        }

        report_path = runner.generate_report_csv()
        content = report_path

        # content already set
        assert "category,test,status,time" in content.lower() or "category,test_name,status,time" in content.lower() or "test_name,category,status,time" in content.lower()
        assert "test_a.py,cat1,PASS" in content or "cat1,test_a.py,PASS" in content

def test_menu_methods_basic(tmp_path):
    config = xyz.TestConfig("dummy")
    with patch("xyz_test_runner.OllamaManager"):
        runner = xyz.TestRunner(str(tmp_path), config)
        menu = xyz.Menu(runner)

        # Test basic UI string replacements / formats working without blowing up
        assert isinstance(xyz.TEXTS["en"]["title"], str)

        with patch("sys.stdout"):
            menu.header()

def test_menu_detect_framework(tmp_path):
    config = xyz.TestConfig("dummy")
    with patch("xyz_test_runner.OllamaManager"):
        runner = xyz.TestRunner(str(tmp_path), config)
        menu = xyz.Menu(runner)

        # Test detection logic
        (tmp_path / "package.json").touch()
        (tmp_path / "pytest.ini").touch()

        with patch.object(menu, 'select_single_interactive', return_value=0):
            # 0 index is typically "Auto-detect" which returns the first detected
            detected = menu.detect_or_select_framework(tmp_path)
            assert detected in ["pytest", "jest"]
