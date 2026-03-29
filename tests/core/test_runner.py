#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for TestRunner class in xyz-test-runner
#xyz-rainbow #rainbowtechnology.xyz #i-love-you
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import importlib.util

import pytest

# Cargar el script como un módulo
script_path = Path(__file__).parent.parent.parent / "scripts" / "xyz-test-runner.py"
spec = importlib.util.spec_from_file_location("xyz_test_runner", str(script_path))
xyz = importlib.util.module_from_spec(spec)
spec.loader.exec_module(xyz)

# #xyz-rainbow #rainbowtechnology.xyz #i-love-you

class TestRunnerImplementation:
    """Pruebas para la clase TestRunner."""

    def setup_method(self):
        """Setup con un entorno de tests falso."""
        self.temp_dir = tempfile.mkdtemp()
        self.base_dir = Path(self.temp_dir)
        
        # Crear estructura de tests: tests/category1/test_a.py
        self.tests_dir = self.base_dir / "tests"
        self.tests_dir.mkdir()
        
        self.cat1_dir = self.tests_dir / "category1"
        self.cat1_dir.mkdir()
        
        with open(self.cat1_dir / "test_a.py", "w") as f:
            f.write("def test_a(): assert True\n")
            
        with open(self.cat1_dir / "not_a_test.py", "w") as f:
            f.write("def helper(): pass\n")
            
        # Crear configuración mínima
        self.config = xyz.TestConfig("")
        self.config.values["TEST_DIR"] = "tests"

    def teardown_method(self):
        """Limpieza."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_discovery(self):
        """Verifica que se descubran los tests correctamente."""
        runner = xyz.TestRunner(str(self.base_dir), self.config)
        runner.discover_categories_and_tests()
        
        assert len(runner.categories) == 1
        cat_key = list(runner.categories.keys())[0]
        cat = runner.categories[cat_key]
        
        assert cat["name"] == "category1"
        assert "test_a.py" in cat["tests"]
        assert "not_a_test.py" not in cat["tests"]

    def test_select_all(self):
        """Verifica la selección de todos los tests."""
        runner = xyz.TestRunner(str(self.base_dir), self.config)
        runner.discover_categories_and_tests()
        runner.select_all()
        
        assert len(runner.selected_tests) == 1
        cat_key = list(runner.categories.keys())[0]
        assert "test_a.py" in runner.selected_tests[cat_key]
