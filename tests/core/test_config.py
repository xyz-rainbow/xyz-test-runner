#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for TestConfig class in xyz-test-runner
#xyz-rainbow #rainbowtechnology.xyz #i-love-you
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import importlib.util

import pytest

# Cargar el script como un módulo a pesar del guion en el nombre
script_path = Path(__file__).parent.parent.parent / "scripts" / "xyz-test-runner.py"
spec = importlib.util.spec_from_file_location("xyz_test_runner", str(script_path))
xyz = importlib.util.module_from_spec(spec)
spec.loader.exec_module(xyz)

# #xyz-rainbow #rainbowtechnology.xyz #i-love-you

class TestConfigImplementation:
    """Pruebas para la clase TestConfig."""

    def setup_method(self):
        """Setup con un archivo de configuración temporal."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "config_test")
        
        with open(self.config_file, "w") as f:
            f.write("LANGUAGE=es\n")
            f.write("USE_IA=true\n")
            f.write("DEFAULT_MODEL=test-model\n")
            f.write("IA_TEMPERATURE=0.5\n")

    def teardown_method(self):
        """Limpieza."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_config(self):
        """Verifica que se carguen los valores correctamente."""
        config = xyz.TestConfig(self.config_file)
        assert config.get("LANGUAGE") == "es"
        assert config.get("DEFAULT_MODEL") == "test-model"
        assert config.get_bool("USE_IA") is True

    def test_default_values(self):
        """Verifica los valores por defecto cuando no existe el archivo."""
        config = xyz.TestConfig("/path/to/nonexistent/config")
        assert config.get("LANGUAGE") == "en"  # Valor por defecto en set_defaults()
        assert config.get_bool("USE_IA") is False

    def test_get_bool(self):
        """Verifica la conversión de booleanos."""
        config = xyz.TestConfig(self.config_file)
        
        # Casos verdaderos
        config.values["TEST_TRUE_1"] = "true"
        config.values["TEST_TRUE_2"] = "yes"
        config.values["TEST_TRUE_3"] = "1"
        config.values["TEST_TRUE_4"] = "si"
        
        assert config.get_bool("TEST_TRUE_1") is True
        assert config.get_bool("TEST_TRUE_2") is True
        assert config.get_bool("TEST_TRUE_3") is True
        assert config.get_bool("TEST_TRUE_4") is True
        
        # Casos falsos
        config.values["TEST_FALSE"] = "false"
        assert config.get_bool("TEST_FALSE") is False
        assert config.get_bool("NONEXISTENT") is False

    def test_save_config(self):
        """Verifica que se pueda guardar la configuración."""
        config = xyz.TestConfig(self.config_file)
        config.values["NEW_KEY"] = "new_value"
        config.save()
        
        # Leer de nuevo para verificar persistencia
        new_config = xyz.TestConfig(self.config_file)
        assert new_config.get("NEW_KEY") == "new_value"
        assert new_config.get("LANGUAGE") == "es"
