#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ═══════════════════════════════════════════════════════════════════════════════════
# ▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
# ▐                             ▌
# ▐    __  __ __   __  _____    ▌
# ▐    \ \/ / \ \ / / |__  /    ▌
# ▐     \  /   \ V /    / /     ▌
# ▐     /  \    | |    / /_     ▌
# ▐    /_/\_\   |_|   /____|    ▌
# ▐                             ▌
# ▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌
#
# xyz-test-runner v2.0 - Universal Test Runner
# #xyz-rainbow #rainbowtechnology.xyz #i-love-you
# ═══════════════════════════════════════════════════════════════════════════════════

import os
import sys
import subprocess
import time
import requests
import base64
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

try:
    import tty
    import termios

    HAS_TTY = True
except ImportError:
    HAS_TTY = False

# #xyz-rainbowtechnology #rainbow.xyz #You're not supposed to see this!

# ════════════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════════════
# ARTE ASCII
# ════════════════════════════════════════════════════════════════════════════════════

# XYZ Grande (Inicio)
ASCII_XYZ = r"""#  __  ____   _______
#  \ \/ /\ \ / /__  /
#   \  /  \ V /  / / 
#   /  \   | |  / /_ 
#  /_/\_\  |_| /____|
"""

# XYZ Rainbow (Reportes e inicio)
ASCII_RAINBOW = r"""┌────────────────────────────────────────────────────────────────┐
│                                  _       _                     │
│   __  ___   _ ____     _ __ __ _(_)_ __ | |__   _____      __  │
│   \ \/ / | | |_  /____| '__/ _` | | '_ \| '_ \ / _ \ \ /\ / /  │
│    >  <| |_| |/ /_____| | | (_| | | | | | |_) | (_) \ V  V /   │
│   /_/\_\\__, /___|    |_|  \__,_|_|_| |_|_.__/ \___/ \_/\_/    │
│         |___/                                                  │
└────────────────────────────────────────────────────────────────┘"""

# XYZ Signature (Final de reportes y script)
ASCII_SIGNATURE = r"""┌────────────────────────────────────────────────────────────────┐
│                                  _       _                     │
│   __  ___   _ ____     _ __ __ _(_)_ __ | |__   _____      __  │
│   \ \/ / | | |_  /____| '__/ _` | | '_ \| '_ \ / _ \ \ /\ / /  │
│    >  <| |_| |/ /_____| | | (_| | | | | | |_) | (_) \ V  V /   │
│   /_/\_\\__, /___|    |_|  \__,_|_|_| |_|_.__/ \___/ \_/\_/    │
│         |___/                                                  │
└────────────────────────────────────────────────────────────────┘"""

# XYZ Box (Antes/después de cada test)
ASCII_XYZ_BOX = r"""# ▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
# ▐                             ▌
# ▐    __  __ __   __  _____    ▌
# ▐    \ \/ / \ \ / / |__  /    ▌
# ▐     \  /   \ V /    / /     ▌
# ▐     /  \    | |    / /_     ▌
# ▐    /_/\_\   |_|   /____|    ▌
# ▐                             ▌
# ▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌"""


def decode_ascii(encoded: str) -> str:
    """Retorna el arte ASCII directamente."""
    return encoded


def show_xyz():
    """Muestra el logo XYZ."""
    print(decode_ascii(ASCII_XYZ))


def show_xyz_box():
    """Muestra el logo XYZ encuadrado."""
    print(decode_ascii(ASCII_XYZ_BOX))


def show_rainbow():
    """Muestra el logo Rainbow en Cian Neon."""
    print(f"{Colors.NEON_CYAN}{decode_ascii(ASCII_RAINBOW)}{Colors.RESET}")


def show_footer():
    """Muestra la firma completa al final en Purpura Neon."""
    print(f"{Colors.NEON_PURPLE}{decode_ascii(ASCII_RAINBOW)}{Colors.RESET}")
    print(f"{Colors.NEON_PURPLE}{decode_ascii(ASCII_SIGNATURE)}{Colors.RESET}")


# #rainbow@rainbowtechnology.xyz #i-love-you

# ════════════════════════════════════════════════════════════════════════════════════
# COLORES Y TEXTOS
# ════════════════════════════════════════════════════════════════════════════════════


class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BG_BLACK = "\033[40m"
    BG_PURPLE = "\033[45m"

    # Neon variants
    NEON_PURPLE = "\033[38;5;171m"
    NEON_CYAN = "\033[38;5;51m"
    NEON_LIME = "\033[38;5;118m"
    NEON_PINK = "\033[38;5;201m"

    @staticmethod
    def neon_print(text: str, color: str = ""):
        """Imprime texto con efecto neon si es posible."""
        if not color:
            color = Colors.NEON_CYAN
        print(f"{color}{Colors.BOLD}{text}{Colors.RESET}")


TEXTS = {
    "es": {
        "title": "xyz-test-runner v2.0 ",
        "select_lang": "Selecciona idioma:",
        "option": "Selecciona opcion:",
        "config": "CONFIGURACION",
        "select_tests": "SELECCIONAR TESTS",
        "execute": "EJECUTAR TESTS",
        "results": "RESULTADOS",
        "generate": "GENERAR REPORTES",
        "exit": "Salir",
        "ia": "IA",
        "back": "Volver",
        "configure_ia": "CONFIGURAR IA",
        "configure_mode": "MODO",
        "select_all": "Seleccionar todos",
        "deselect_all": "Deseleccionar todos",
        "confirm": "Confirmar",
        "total": "Total",
        "start": "Comenzar?",
        "running": "EJECUTANDO",
        "no_tests": "No hay tests seleccionados",
        "complete": "Ejecucion completada",
        "generating": "GENERANDO REPORTES",
        "tests": "tests",
        "category": "CATEGORIAS",
        "enter": "Presiona Enter...",
        "configure_gpu": "PROTECCION GPU",
        "gpu_protection_active": "GPU Protection ACTIVA - Tests de motor excluidos",
        "gpu_protection_excluded": "GPU Protection activa: test(s) de motor excluido(s)",
        "configure_xvfb": "Xvfb (SIN PANTALLA)",
        "xvfb_active": "Xvfb ACTIVO - Tests sin afectar GNOME",
        "ai_analyze": "Analizar con IA?",
        "ai_yes": "Si - Generar interpretacion IA",
        "ai_no": "No - Saltar",
        "ai_generating": "Generando interpretacion IA con",
        "open_reports": "Abrir reportes?",
        "open_yes": "Si - Abrir con aplicacion predeterminada",
        "open_no": "No - Continuar",
        "create_ai": "Crear Tests con IA",
        "select_folder": "Seleccionar Carpeta",
        "current_folder": "Usar carpeta del proyecto actual",
        "custom_folder": "Introducir ruta personalizada",
        "enter_path": "Introduce la ruta de la carpeta:",
        "invalid_path": "Ruta invalida",
        "scan_files": "Escaneando archivos del proyecto...",
        "select_files": "Selecciona archivos para analizar",
        "framework": "Framework de Tests",
        "select_framework": "Selecciona el framework de tests:",
        "select_model": "Selecciona el modelo de IA para generar tests",
        "custom_model": "Introducir modelo personalizado",
        "enter_model": "Introduce el nombre del modelo:",
        "select_category": "Selecciona la categoria de los tests:",
        "generating_tests": "Generando Tests...",
        "saving_tests": "Tests guardados en:",
        "move_select": "[↑/↓/1-9] Mover/Sel  [Enter] Confirmar  [Esc/V] Volver",
        "move_toggle": "[↑/↓/1-9] Mover/Alt  [Space] Alternar  [Enter] Confirmar  [Esc/V] Volver",
        "select_formats_label": "📝 Seleccionar Formatos de Exportacion (Flechas + Espacio)",
        "move_toggle_formats": "[↑/↓/1-4] Mover/Alt  [Space] Alternar  [Enter] Generar  [Esc/V] Volver",
    },
    "en": {
        "title": "xyz-test-runner v2.0 ",
        "select_lang": "Select language:",
        "option": "Select option:",
        "config": "SETTINGS",
        "select_tests": "SELECT TESTS",
        "execute": "RUN TESTS",
        "results": "RESULTS",
        "generate": "GENERATE REPORTS",
        "exit": "Exit",
        "ia": "AI",
        "back": "Back",
        "configure_ia": "CONFIGURE AI",
        "configure_mode": "MODE",
        "select_all": "Select all",
        "deselect_all": "Deselect all",
        "confirm": "Confirm",
        "total": "Total",
        "start": "Start?",
        "running": "RUNNING",
        "no_tests": "No tests selected",
        "complete": "Execution complete",
        "generating": "GENERATING REPORTS",
        "tests": "tests",
        "category": "CATEGORIES",
        "enter": "Press Enter...",
        "configure_gpu": "GPU PROTECTION",
        "gpu_protection_active": "GPU Protection ACTIVE - Motor tests excluded",
        "gpu_protection_excluded": "GPU Protection active: motor test(s) excluded",
        "configure_xvfb": "Xvfb (HEADLESS)",
        "xvfb_active": "Xvfb ACTIVE - Tests without affecting GNOME",
        "ai_analyze": "Analyze with AI?",
        "ai_yes": "Yes - Generate AI interpretation",
        "ai_no": "No - Skip",
        "ai_generating": "Generating AI interpretation with",
        "open_reports": "Open reports?",
        "open_yes": "Yes - Open with default app",
        "open_no": "No - Continue",
        "create_ai": "Create Tests with AI",
        "select_folder": "Select Folder",
        "current_folder": "Use current project folder",
        "custom_folder": "Enter custom path",
        "enter_path": "Enter folder path:",
        "invalid_path": "Invalid path",
        "scan_files": "Scanning project files...",
        "select_files": "Select files to analyze",
        "framework": "Test Framework",
        "select_framework": "Select test framework:",
        "select_model": "Select AI Model for Test Generation",
        "custom_model": "Enter custom model",
        "enter_model": "Enter model name:",
        "select_category": "Select test category:",
        "generating_tests": "Generating Tests...",
        "saving_tests": "Tests saved to:",
        "move_select": "[↑/↓/1-9] Move/Select  [Enter] Confirm  [Esc/V] Back",
        "move_toggle": "[↑/↓/1-9] Move/Toggle  [Space] Toggle  [Enter] Confirm  [Esc/V] Back",
        "select_formats_label": "📝 Select Export Formats (Arrow Keys + Space)",
        "move_toggle_formats": "[↑/↓/1-4] Move/Toggle  [Space] Toggle  [Enter] Generate  [Esc/V] Back",
    },
}

# ════════════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DEL SISTEMA
# ════════════════════════════════════════════════════════════════════════════════════


class TestConfig:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.values = {}
        self.load()

    def load(self):
        """Carga la configuración desde el archivo."""
        if not os.path.exists(self.config_path):
            self.set_defaults()
            return
        with open(self.config_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    self.values[key.strip()] = value.strip()

    def set_defaults(self):
        """Valores por defecto si no hay archivo de configuración."""
        # #xyz-rainbow #rainbowtechnology.xyz #i-love-you
        self.values = {
            "LANGUAGE": "en",
            "USE_IA": "false",
            "DEFAULT_MODEL": "qwen3.5:0.8b",
            "IA_TEMPERATURE": "0.3",
            "EXECUTION_MODE": "sequential",
            "PARALLEL_WORKERS": "4",
            "TERMINAL_VISIBLE": "true",
            "SAVE_RAW_OUTPUTS": "true",
            "TEST_DIR": "tests",
            "REPORT_DIR": "reportes",
            "FINAL_REPORT_RAW": "TEST_REPORT_SUMMARY.md",
            "FINAL_REPORT_MODEL": "TEST_REPORT_SUMMARY_MODEL.md",
            "OLLAMA_HOST": "http://localhost:11434",
            "OLLAMA_TIMEOUT": "60",
            "REPORT_DETAIL_LEVEL": "full",
            "EXPORT_FORMATS": "md,html,csv",
            "SHOW_SIGNATURE": "true",
            "GPU_PROTECTION": "false",
            "SIGNATURE_TEXT": "#xyz-rainbow #rainbowtechnology.xyz #i-love-you",
        }
        # #You're not supposed to see this! #rainbow@rainbowtechnology.xyz

    def get(self, key: str, default: str = "") -> str:
        return self.values.get(key, default)

    def get_bool(self, key: str, default: bool = False) -> bool:
        return self.values.get(key, "").lower() in ("true", "yes", "1", "si", "s")

    def save(self):
        """Guarda la configuración en el archivo."""
        if not self.config_path:
            return
        lines = []
        for key, value in self.values.items():
            lines.append(f"{key}={value}")
        with open(self.config_path, "w") as f:
            f.write(
                "# ════════════════════════════════════════════════════════════════════════════\n"
            )
            f.write("# xyz-test-runner CONFIGURATION\n")
            f.write("# #xyz-rainbow #rainbowtechnology.xyz #i-love-you\n")
            f.write(
                "# ════════════════════════════════════════════════════════════════════════════\n"
            )
            f.write("\n")
            f.write("\n".join(lines))
            f.write("\n")


# #xyz-rainbow #rainbowtechnology.xyz #i-love-you

# ════════════════════════════════════════════════════════════════════════════════════
# GESTIÓN DE OLLAMA (IA)
# ════════════════════════════════════════════════════════════════════════════════════


class OllamaManager:
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
        self.models = []
        self.available = False
        self.check_connection()

    def check_connection(self):
        """Verifica si el servidor de Ollama está activo."""
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=5)
            if r.status_code == 200:
                self.available = True
                self.models = [m["name"] for m in r.json().get("models", [])]
        except:
            self.available = False

    def generate(
        self, model: str, prompt: str, system: str = "", temperature: float = 0.3
    ) -> Optional[str]:
        """Genera una interpretación de los resultados usando IA."""
        if not self.available:
            return None
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature},
            }
            if system:
                payload["system"] = system
            r = requests.post(f"{self.host}/api/generate", json=payload, timeout=120)
            if r.status_code == 200:
                return r.json().get("response", "")
        except Exception as e:
            print(f"{Colors.RED}Error IA: {e}{Colors.RESET}")
        return None


# #You're not supposed to see this! #xyz-rainbowtechnology

# ════════════════════════════════════════════════════════════════════════════════════
# MOTOR DE EJECUCIÓN DE TESTS
# ════════════════════════════════════════════════════════════════════════════════════


class TestRunner:
    def __init__(self, base_dir: str, config: TestConfig, language: str = "en"):
        self.base_dir = Path(base_dir)
        self.config = config
        self.language = language
        self.ollama = OllamaManager(config.get("OLLAMA_HOST"))

        self.selected_tests = {}
        self.results = {}
        self.report_dir = None
        self.categories = {}

    def discover_categories_and_tests(self):
        """Descubre categorías y archivos de test automáticamente."""
        tests_dir = self.base_dir / self.config.get("TEST_DIR", "tests")

        if not tests_dir.exists():
            print(
                f"{Colors.RED}Directorio de tests no encontrado: {tests_dir}{Colors.RESET}"
            )
            return

        for i, cat_dir in enumerate(sorted(tests_dir.iterdir()), 1):
            if cat_dir.is_dir() and not cat_dir.name.startswith("_"):
                tests = [f.name for f in cat_dir.glob("test_*.py")]
                if tests:
                    self.categories[str(i)] = {
                        "name": cat_dir.name,
                        "path": str(cat_dir.relative_to(self.base_dir)),
                        "tests": sorted(tests),
                        "enabled": True,
                    }

    def select_all(self):
        """Selecciona todos los tests descubiertos."""
        gpu_protection = self.config.get_bool("GPU_PROTECTION")

        for key, cat in self.categories.items():
            if cat["enabled"]:
                tests = cat["tests"][:]

                if gpu_protection:
                    original_count = len(tests)
                    tests = [t for t in tests if "motor" not in t.lower()]
                    removed = original_count - len(tests)
                    if removed > 0:
                        msg = TEXTS.get(self.language, TEXTS["en"]).get(
                            "gpu_protection_excluded",
                            "GPU Protection active: motor test(s) excluded",
                        )
                        print(f"\n{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

                self.selected_tests[key] = tests

    def deselect_all(self):
        """Deselecciona todos los tests."""
        self.selected_tests = {}

    def toggle_test(self, category: str, test: str):
        """Activa/Desactiva un test específico."""
        if category not in self.selected_tests:
            self.selected_tests[category] = []
        if test in self.selected_tests[category]:
            self.selected_tests[category].remove(test)
        else:
            self.selected_tests[category].append(test)

    def run_test(self, category: str, test: str, verbose: bool = True) -> Dict:
        """Ejecuta un archivo de test usando pytest."""
        test_path = self.base_dir / self.categories[category]["path"] / test

        cmd = [
            "python3",
            "-m",
            "pytest",
            str(test_path),
            "-v",
            "--tb=short",
            "--color=no",
        ]

        use_xvfb = self.config.get_bool("XVFB")
        if use_xvfb:
            cmd = ["xvfb-run", "-a"] + cmd

        result = {
            "category": category,
            "test": test,
            "test_path": str(test_path),
            "result": "ERROR",
            "output": "",
            "time": 0,
            "passed": 0,
            "failed": 0,
            "individual_tests": [],
        }

        try:
            if verbose:
                show_xyz_box()
                print(
                    f"  {Colors.NEON_CYAN}▶{Colors.RESET} {test}...",
                    end=" ",
                    flush=True,
                )

            start = time.time()

            env = os.environ.copy()
            if self.config.get_bool("GPU_PROTECTION"):
                env["NVIDIA_VISIBLE_DEVICES"] = "off"
                env["CUDA_VISIBLE_DEVICES"] = ""
                env["VIDEO_STUDIO_FORCE_SOFTWARE_CODEC"] = "libx264"

            proc = subprocess.run(
                cmd,
                cwd=str(self.base_dir),
                capture_output=True,
                text=True,
                timeout=300,
                env=env,
            )
            result["time"] = time.time() - start
            result["output"] = proc.stdout + proc.stderr

            for line in result["output"].split("\n"):
                if "PASSED" in line or "FAILED" in line or "ERROR" in line:
                    result["individual_tests"].append(line.strip())

            if proc.returncode == 0:
                result["result"] = "PASS"
                if verbose:
                    print(f"{Colors.NEON_LIME}✓{Colors.RESET}")
            else:
                result["result"] = "FAIL"
                if verbose:
                    print(f"{Colors.NEON_PINK}✗{Colors.RESET}")

        except subprocess.TimeoutExpired:
            result["result"] = "TIMEOUT"
            if verbose:
                print(f"{Colors.YELLOW}⏱{Colors.RESET}")
        except Exception as e:
            result["result"] = "ERROR"
            if verbose:
                print(f"{Colors.RED}⚠{Colors.RESET}: {e}")

        return result

    def run_all_selected(self, verbose: bool = True) -> Dict:
        """Ejecuta la cola de tests seleccionados."""
        self.results = {}
        total = sum(len(t) for t in self.selected_tests.values())

        gpu_protection = self.config.get_bool("GPU_PROTECTION")
        if gpu_protection:
            msg = TEXTS.get(self.language, TEXTS["en"]).get(
                "gpu_protection_active", "GPU Protection ACTIVE - Motor tests excluded"
            )
            print(f"\n{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

        current = 0

        for category, tests in self.selected_tests.items():
            for test in tests:
                # Si GPU Protection está activa, saltar tests que tengan 'motor' en el nombre
                if gpu_protection and "motor" in test.lower():
                    msg_excl = TEXTS.get(self.language, TEXTS["en"]).get(
                        "gpu_protection_excluded",
                        "GPU Protection active: motor test(s) excluded",
                    )
                    print(
                        f"{Colors.YELLOW}⏩ Skipping {test} ({msg_excl}){Colors.RESET}"
                    )
                    continue

                current += 1
                if verbose:
                    print(f"\n{Colors.BOLD}[{current}/{total}]{Colors.RESET}")
                result = self.run_test(category, test, verbose)
                self.results[f"{category}/{test}"] = result

        return self.results

    def generate_report_raw(self, detail_level: str = "full") -> str:
        """Genera el contenido del reporte en Markdown."""
        lines = []
        lines.append(decode_ascii(ASCII_RAINBOW))
        lines.append(f"# Test Report - xyz-test-runner v2.0")
        lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        passed = sum(1 for r in self.results.values() if r["result"] == "PASS")
        failed = sum(1 for r in self.results.values() if r["result"] == "FAIL")

        lines.append(f"\n## Summary")
        lines.append(f"- **Passed:** {passed}")
        lines.append(f"- **Failed:** {failed}")

        lines.append(f"\n## All Tests")
        for cat_key, cat in self.categories.items():
            cat_results = {
                k: v for k, v in self.results.items() if k.startswith(cat_key + "/")
            }
            if cat_results:
                lines.append(f"\n### {cat['name'].upper()}")
                for key, result in cat_results.items():
                    test_name = key.split("/")[1]
                    icon = "✓" if result["result"] == "PASS" else "✗"
                    lines.append(f"- {icon} **{test_name}** ({result['time']:.2f}s)")

        lines.append(f"\n\n---\n")
        lines.append(decode_ascii(ASCII_RAINBOW))
        lines.append(decode_ascii(ASCII_SIGNATURE))
        lines.append(
            f"\n*Generated by xyz-test-runner v2.0 | #xyz-rainbow #rainbowtechnology.xyz*"
        )
        return "\n".join(lines)

    def generate_report_html(self, detail_level: str = "full") -> str:
        """Genera el reporte en formato HTML con el estilo oficial XYZ - Rainbow Technology."""
        passed = sum(1 for r in self.results.values() if r["result"] == "PASS")
        failed = sum(1 for r in self.results.values() if r["result"] == "FAIL")
        total = len(self.results)
        pct = (passed / total * 100) if total > 0 else 0

        # #xyz-rainbow #rainbowtechnology.xyz
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XYZ Test Report - {datetime.now().strftime("%Y-%m-%d")}</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <div class="container">
        <img src="../assets/banner.svg" alt="XYZ Rainbow Technology" class="header-banner">
        
        <h1>Test Execution Report</h1>
        
        <div class="summary-grid">
            <div class="stat-item">
                <span class="stat-val val-total">{total}</span>
                <span class="stat-label">Total Tests</span>
            </div>
            <div class="stat-item">
                <span class="stat-val val-pass">{passed}</span>
                <span class="stat-label">Passed</span>
            </div>
            <div class="stat-item">
                <span class="stat-val val-fail">{failed}</span>
                <span class="stat-label">Failed</span>
            </div>
        </div>
        
        <div class="test-list">"""

        for k, r in self.results.items():
            status = r["result"]
            test_name = k.split("/")[-1]
            badge_class = "badge-pass" if status == "PASS" else "badge-fail"
            
            html += f"""
            <div class="test-card">
                <div class="test-info">
                    <span class="test-name">{test_name}</span>
                    <span class="test-meta">Execution time: {r["time"]:.3f}s | {k}</span>
                </div>
                <span class="badge {badge_class}">{status}</span>
            </div>"""

        html += f"""
        </div>
        
        <footer>
            <p>Generated by <strong>xyz-test-runner v2.0</strong> on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <div class="signature">
                #xyz-rainbow<br>
                #rainbowtechnology.xyz<br>
                #i-love-you
            </div>
        </footer>
    </div>
</body>
</html>"""
        # #You're not supposed to see this!
        return html
        return html

    def generate_report_csv(self) -> str:
        """Genera el reporte en formato CSV."""
        lines = ["test_name,category,status,time"]
        for key, result in self.results.items():
            cat_key, test = key.split("/")
            cat_name = self.categories[cat_key]["name"]
            lines.append(f"{test},{cat_name},{result['result']},{result['time']:.2f}")
        return "\n".join(lines)


# #rainbow.xyz #i-love-you #xyz-rainbow

# ════════════════════════════════════════════════════════════════════════════════════
# INTERFAZ DE MENÚ (TUI)
# ════════════════════════════════════════════════════════════════════════════════════


class Menu:
    def __init__(self, runner: TestRunner):
        self.runner = runner
        self.running = True
        self.language = self.runner.config.get("LANGUAGE", "en")

    def clear(self):
        """Limpia la terminal."""
        os.system("clear" if os.name == "posix" else "cls")

    def get_key(self):
        """Get a single keypress. Returns key name or character."""
        if not HAS_TTY:
            return input("")[0] if hasattr(input, "__call__") else ""

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                seq = sys.stdin.read(2)
                if seq == "[A":
                    return "UP"
                elif seq == "[B":
                    return "DOWN"
                elif seq == "[C":
                    return "RIGHT"
                elif seq == "[D":
                    return "LEFT"
                elif seq == " ":
                    return "SPACE"
                return "ESC"
            elif ch == "\n":
                return "ENTER"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def select_formats_interactive(
        self, formats_list: List[str], current_selected: List[str]
    ) -> Optional[List[str]]:
        """Interactive format selection with arrow keys and space."""
        selected = [fmt in current_selected for fmt in formats_list]
        cursor = 0

        while True:
            self.header()
            print(
                f"{Colors.CYAN}{TEXTS[self.language]['select_formats_label']}{Colors.RESET}\n"
            )

            for i, fmt in enumerate(formats_list):
                if i == cursor:
                    print(f"  {Colors.YELLOW}▶{Colors.RESET} ", end="")
                else:
                    print(f"    ", end="")

                if selected[i]:
                    print(f"{Colors.GREEN}●{Colors.RESET} [{fmt.upper()}]")
                else:
                    print(f" {Colors.GRAY}○{Colors.RESET}  [{fmt.upper()}]")

            print(
                f"\n  {Colors.CYAN}{TEXTS[self.language]['move_toggle_formats']}{Colors.RESET}"
            )

            key = self.get_key()

            if key == "UP" and cursor > 0:
                cursor -= 1
            elif key == "DOWN" and cursor < len(formats_list) - 1:
                cursor += 1
            elif key.isdigit() and 1 <= int(key) <= len(formats_list):
                idx = int(key) - 1
                selected[idx] = not selected[idx]
            elif key == "SPACE":
                selected[cursor] = not selected[cursor]
            elif key == "ENTER":
                return [formats_list[i] for i, s in enumerate(selected) if s]
            elif key in ("ESC", "v", "q"):
                return None

    def select_single_interactive(
        self, title: str, options: List[str], current: Optional[int] = None
    ) -> Optional[int]:
        """Interactive single selection with arrow keys and enter."""
        cursor = current if current is not None else 0

        while True:
            self.header()
            print(f"{Colors.CYAN}{title}{Colors.RESET}\n")

            for i, opt in enumerate(options):
                if i == cursor:
                    print(f"  {Colors.YELLOW}▶{Colors.RESET} {opt}")
                else:
                    print(f"     {opt}")

            print(
                f"\n  {Colors.CYAN}{TEXTS[self.language]['move_select']}{Colors.RESET}"
            )

            key = self.get_key()

            if key == "UP" and cursor > 0:
                cursor -= 1
            elif key == "DOWN" and cursor < len(options) - 1:
                cursor += 1
            elif key.isdigit() and 1 <= int(key) <= len(options):
                return int(key) - 1
            elif key == "ENTER":
                return cursor
            elif key in ("ESC", "v", "q", "b"):
                return None

    def select_multiple_interactive(
        self, title: str, options: List[str], selected: Optional[List[bool]] = None
    ) -> Optional[List[bool]]:
        """Interactive multi-selection with arrow keys and space."""
        if selected is None:
            selected = [False] * len(options)
        cursor = 0

        while True:
            self.header()
            print(f"{Colors.CYAN}{title}{Colors.RESET}\n")

            for i, opt in enumerate(options):
                if i == cursor:
                    print(f"  {Colors.YELLOW}▶{Colors.RESET} ", end="")
                else:
                    print(f"    ", end="")

                if selected[i]:
                    print(f"{Colors.GREEN}●{Colors.RESET} {opt}")
                else:
                    print(f" {Colors.GRAY}○{Colors.RESET}  {opt}")

            print(
                f"\n  {Colors.CYAN}{TEXTS[self.language]['move_toggle']}{Colors.RESET}"
            )

            key = self.get_key()

            if key == "UP" and cursor > 0:
                cursor -= 1
            elif key == "DOWN" and cursor < len(options) - 1:
                cursor += 1
            elif key.isdigit() and 1 <= int(key) <= len(options):
                idx = int(key) - 1
                selected[idx] = not selected[idx]
            elif key == "SPACE":
                selected[cursor] = not selected[cursor]
            elif key == "ENTER":
                return selected
            elif key in ("ESC", "v", "q", "b"):
                return None

    def header(self):
        """Muestra la cabecera del menú con efecto Neon."""
        self.clear()
        show_rainbow()
        print(f"{Colors.NEON_PURPLE}{Colors.BOLD}")
        print("╔════════════════════════════════════════════════════════════╗")
        print(
            f"║         {Colors.WHITE}{TEXTS[self.language]['title']:44s}{Colors.NEON_PURPLE}║"
        )
        print("╚════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")

    def select_language(self):
        """Permite al usuario elegir el idioma."""
        while True:
            self.header()
            print(f"{Colors.CYAN}{TEXTS[self.language]['select_lang']}{Colors.RESET}\n")
            print(f"  [1] English")
            print(f"  [2] Espanol")
            print()
            choice = input(f"{Colors.YELLOW}>> {Colors.RESET}").strip()
            if choice in ("1", ""):
                self.language = "en"
                break
            elif choice == "2":
                self.language = "es"
                break
        self.runner.config.values["LANGUAGE"] = self.language
        self.runner.config.save()
        return self.language

    def main_menu(self):
        """Menú principal de la aplicación."""
        menu_options = [
            TEXTS[self.language]["config"],
            TEXTS[self.language]["select_tests"],
            TEXTS[self.language]["execute"],
            TEXTS[self.language]["results"],
            TEXTS[self.language]["generate"],
            TEXTS[self.language]["create_ai"],
            TEXTS[self.language]["exit"],
        ]

        while self.running:
            result = self.select_single_interactive(
                TEXTS[self.language]["option"], menu_options
            )
            if result is None:
                show_footer()
                break
            elif result == 6:
                show_footer()
                break
            elif result == 0:
                self.config_menu()
            elif result == 1:
                self.select_tests_menu()
            elif result == 2:
                self.execute_menu()
            elif result == 3:
                self.results_menu()
            elif result == 4:
                self.generate_menu()
            elif result == 5:
                self.create_tests_menu()

    def config_menu(self):
        """Menú de configuración de parámetros."""
        while True:
            use_ia = self.runner.config.get_bool("USE_IA")
            mode = self.runner.config.get("EXECUTION_MODE", "sequential")
            gpu_prot = self.runner.config.get_bool("GPU_PROTECTION")
            xvfb = self.runner.config.get_bool("XVFB")
            gpu_label = TEXTS[self.language].get("configure_gpu", "GPU Protection")
            xvfb_label = TEXTS[self.language].get("configure_xvfb", "Xvfb (HEADLESS)")

            config_options = [
                f"AI: {'ON' if use_ia else 'OFF'}",
                f"Mode: {mode}",
                f"GPU: {'ON' if gpu_prot else 'OFF'}",
                f"Xvfb: {'ON' if xvfb else 'OFF'}",
                TEXTS[self.language]["back"],
            ]

            result = self.select_single_interactive(
                TEXTS[self.language]["config"], config_options
            )
            if result is None or result == 4:
                print(f"{Colors.YELLOW}{TEXTS[self.language]['back']}{Colors.RESET}")
                break
            choice = str(result + 1)

            if choice == "1":
                self.runner.config.values["USE_IA"] = "false" if use_ia else "true"
                self.runner.config.save()
                print(
                    f"{Colors.GREEN}✓ AI: {'ON' if not use_ia else 'OFF'}{Colors.RESET}"
                )
                input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")
            elif choice == "2":
                new_mode = "parallel" if mode == "sequential" else "sequential"
                self.runner.config.values["EXECUTION_MODE"] = new_mode
                self.runner.config.save()
                print(f"{Colors.GREEN}✓ Mode: {new_mode}{Colors.RESET}")
                input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")
            elif choice == "3":
                self.runner.config.values["GPU_PROTECTION"] = (
                    "false" if gpu_prot else "true"
                )
                self.runner.config.save()
                print(
                    f"{Colors.GREEN}✓ GPU: {'ON' if not gpu_prot else 'OFF'}{Colors.RESET}"
                )
                input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")
            elif choice == "4":
                self.runner.config.values["XVFB"] = "false" if xvfb else "true"
                self.runner.config.save()
                print(
                    f"{Colors.GREEN}✓ Xvfb: {'ON' if not xvfb else 'OFF'}{Colors.RESET}"
                )
                input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")
            elif choice == "5":
                print(f"{Colors.YELLOW}{TEXTS[self.language]['back']}{Colors.RESET}")
                break

    def select_tests_menu(self):
        """Menú de selección de categorías de test."""
        while True:
            cat_options = []
            for key, cat in self.runner.categories.items():
                icon = "✓" if cat["enabled"] else "✗"
                cat_options.append(f"{icon} {cat['name'].upper()}")

            cat_options.append(f"[E] {TEXTS[self.language]['confirm']}")
            cat_options.append(f"[V] {TEXTS[self.language]['back']}")

            result = self.select_single_interactive(
                TEXTS[self.language]["category"], cat_options
            )
            if result is None or result == len(cat_options) - 1:
                print(f"{Colors.YELLOW}{TEXTS[self.language]['back']}{Colors.RESET}")
                break
            elif result == len(cat_options) - 2:
                self.select_tests_in_categories()
            else:
                key = list(self.runner.categories.keys())[result]
                self.runner.categories[key]["enabled"] = not self.runner.categories[
                    key
                ]["enabled"]
                status = "✓" if self.runner.categories[key]["enabled"] else "✗"
                print(
                    f"{Colors.GREEN}✓{Colors.RESET} {status} {self.runner.categories[key]['name'].upper()}"
                )

    def select_tests_in_categories(self):
        """Selección individual de archivos de test."""
        enabled = [k for k, c in self.runner.categories.items() if c["enabled"]]
        for cat_key in enabled:
            cat = self.runner.categories[cat_key]
            while True:
                test_options = cat["tests"] + [
                    f"[ENTER] {TEXTS[self.language]['confirm']}"
                ]
                result = self.select_single_interactive(
                    f"Select tests: {cat['name'].upper()}", test_options
                )
                if result is None or result == len(test_options) - 1:
                    print(
                        f"{Colors.YELLOW}{TEXTS[self.language]['back']}{Colors.RESET}"
                    )
                    break
                else:
                    test_name = cat["tests"][result]
                    self.runner.toggle_test(cat_key, test_name)
                    is_selected = test_name in self.runner.selected_tests.get(
                        cat_key, []
                    )
                    print(
                        f"{Colors.GREEN}✓{Colors.RESET} {'●' if is_selected else '○'} {test_name}"
                    )

    def execute_menu(self):
        """Menú de ejecución de los tests seleccionados."""
        if not self.runner.selected_tests:
            print(f"{Colors.RED}{TEXTS[self.language]['no_tests']}{Colors.RESET}")
            input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")
            return
        self.header()
        print(f"{Colors.CYAN}▶ {TEXTS[self.language]['running']}{Colors.RESET}\n")
        confirm = input(f"{TEXTS[self.language]['start']} [S/N]: ").strip().lower()
        if confirm in ("s", "y", ""):
            self.runner.run_all_selected()
            print(
                f"\n{Colors.NEON_CYAN}✓ {TEXTS[self.language]['complete']}{Colors.RESET}"
            )
            input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")

    def results_menu(self):
        """Muestra los resultados de la última ejecución."""
        if not self.runner.results:
            print(f"{Colors.YELLOW}No hay resultados{Colors.RESET}")
            input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")
            return
        self.header()
        for key, result in self.runner.results.items():
            color = Colors.GREEN if result["result"] == "PASS" else Colors.RED
            print(f"  {color}●{Colors.RESET} {key.split('/')[1]} - {result['result']}")
        print()
        input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")

    def generate_menu(self):
        """Genera los archivos de reporte en los formatos seleccionados."""
        # #xyz-rainbow #rainbowtechnology.xyz
        if not self.runner.results:
            return

        report_dir_name = self.runner.config.get("REPORT_DIR", "reportes")
        report_path = self.runner.base_dir / report_dir_name
        report_path.mkdir(parents=True, exist_ok=True)

        current_formats = self.runner.config.get("EXPORT_FORMATS", "md,html,csv").split(",")
        formats_list = ["md", "html", "txt", "csv"]

        selected = self.select_formats_interactive(formats_list, current_formats)
        if selected is None:
            return
        current_formats = selected

        if not current_formats:
            print(f"{Colors.RED}No formats selected{Colors.RESET}")
            input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")
            return

        self.runner.config.values["EXPORT_FORMATS"] = ",".join(current_formats)
        self.header()
        print(f"{Colors.CYAN}📝 {TEXTS[self.language]['generating']} in {report_dir_name}/{Colors.RESET}\n")

        generated_files = []

        if "md" in current_formats:
            fname = self.runner.config.get("FINAL_REPORT_RAW", "TEST_REPORT_SUMMARY.md")
            with open(report_path / fname, "w") as f:
                f.write(self.runner.generate_report_raw())
            print(f"✓ MD: {fname}")
            generated_files.append(report_path / fname)

        if "html" in current_formats:
            fname = "TEST_REPORT_SUMMARY.html"
            with open(report_path / fname, "w") as f:
                f.write(self.runner.generate_report_html())
            print(f"✓ HTML: {fname}")
            generated_files.append(report_path / fname)

        if "txt" in current_formats:
            fname = "TEST_REPORT_SUMMARY.txt"
            with open(report_path / fname, "w") as f:
                f.write(self.runner.generate_report_raw())
            print(f"✓ TXT: {fname}")
            generated_files.append(report_path / fname)

        if "csv" in current_formats:
            fname = "TEST_REPORT_SUMMARY.csv"
            with open(report_path / fname, "w") as f:
                f.write(self.runner.generate_report_csv())
            print(f"✓ CSV: {fname}")
            generated_files.append(report_path / fname)

        # #You're not supposed to see this!
        # Preguntar si quiere análisis IA
        print(f"\n{Colors.CYAN}🤖 {TEXTS[self.language]['ai_analyze']}{Colors.RESET}")
        print(f"  [Y] {TEXTS[self.language]['ai_yes']}")
        print(f"  [N] {TEXTS[self.language]['ai_no']}")

        ai_choice = input(f"{Colors.YELLOW}>> {Colors.RESET}").strip().lower()

        if ai_choice in ("y", "yes", "s", "si", ""):
            if self.runner.ollama.available:
                model = self.runner.config.get("DEFAULT_MODEL")
                print(f"\n{Colors.CYAN}🤖 {TEXTS[self.language]['ai_generating']} {model}...{Colors.RESET}")
                interp = self.runner.ollama.generate(
                    model,
                    "Analyze these test results and provide insights: " + self.runner.generate_report_raw(),
                )
                if interp:
                    fname_ai = self.runner.config.get("FINAL_REPORT_MODEL", "TEST_REPORT_SUMMARY_MODEL.md")
                    with open(report_path / fname_ai, "w") as f:
                        f.write(f"# AI Interpretation\n**Model:** {model}\n**Date:** {datetime.now()}\n\n")
                        f.write(interp)
                    print(f"✓ AI: {fname_ai}")
                    generated_files.append(report_path / fname_ai)
                else:
                    print(f"{Colors.RED}✗ AI generation failed{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}⚠ Ollama not available{Colors.RESET}")

        # Preguntar si abrir reportes
        print(f"\n{Colors.CYAN}📂 {TEXTS[self.language]['open_reports']}{Colors.RESET}")
        print(f"  [Y] {TEXTS[self.language]['open_yes']}")
        print(f"  [N] {TEXTS[self.language]['open_no']}")

        open_choice = input(f"{Colors.YELLOW}>> {Colors.RESET}").strip().lower()

        if open_choice in ("y", "yes", "s", "si", ""):
            for filepath in generated_files:
                if filepath.exists():
                    try:
                        subprocess.run(["xdg-open", str(filepath)], check=False)
                    except:
                        pass

        show_footer()
        print()
        input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")

    def create_tests_menu(self):
        """Create tests using AI."""
        self.header()
        print(f"{Colors.CYAN}🤖 {TEXTS[self.language]['create_ai']}{Colors.RESET}\n")

        folder_path = self.select_folder()
        if folder_path is None:
            print(f"{Colors.YELLOW}{TEXTS[self.language]['back']}{Colors.RESET}")
            return

        self.header()
        print(
            f"{Colors.CYAN}📁 {TEXTS[self.language]['total']}: {folder_path}{Colors.RESET}\n"
        )

        source_files = self.scan_project_files(folder_path)
        if not source_files:
            print(f"{Colors.RED}No source files found{Colors.RESET}")
            input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")
            return

        self.header()
        print(f"{Colors.CYAN}📄 {TEXTS[self.language]['select_files']}{Colors.RESET}\n")

        file_names = [str(Path(f).relative_to(folder_path)) for f in source_files]
        selected = self.select_multiple_interactive(
            TEXTS[self.language]["select_files"], file_names
        )

        if selected is None or not any(selected):
            print(f"{Colors.YELLOW}{TEXTS[self.language]['back']}{Colors.RESET}")
            return

        selected_files = [source_files[i] for i, s in enumerate(selected) if s]

        framework = self.detect_or_select_framework(folder_path)

        model = self.select_ai_model()

        print(
            f"\n{Colors.CYAN}📂 {TEXTS[self.language]['select_folder']}{Colors.RESET}\n"
        )
        save_path = self.select_folder()
        if save_path is None:
            print(f"{Colors.YELLOW}{TEXTS[self.language]['back']}{Colors.RESET}")
            return

        category = self.select_test_category()

        self.generate_tests_with_ai(
            selected_files, folder_path, framework, model, save_path, category
        )

    def select_folder(self):
        """Simple folder selection - enter path or use current."""
        self.header()
        print(
            f"{Colors.CYAN}📁 {TEXTS[self.language]['select_folder']}{Colors.RESET}\n"
        )
        print(f"  {TEXTS[self.language]['total']}: {self.runner.base_dir}")
        print(f"\n  [1] {TEXTS[self.language]['current_folder']}")
        print(f"  [2] {TEXTS[self.language]['custom_folder']}")
        print(f"  [V] {TEXTS[self.language]['back']}\n")

        choice = input(f"{Colors.YELLOW}>> {Colors.RESET}").strip().lower()

        if choice == "v":
            return None
        elif choice == "1":
            return Path(self.runner.base_dir)
        elif choice == "2":
            print(f"\n{Colors.CYAN}{TEXTS[self.language]['enter_path']}{Colors.RESET}")
            path = input(f"{Colors.YELLOW}>> {Colors.RESET}").strip()
            if path and Path(path).exists() and Path(path).is_dir():
                return Path(path)
            else:
                print(
                    f"{Colors.RED}{TEXTS[self.language]['invalid_path']}{Colors.RESET}"
                )
                return Path(self.runner.base_dir)
        else:
            return Path(self.runner.base_dir)

    def scan_project_files(self, folder_path):
        """Scan for source files in folder."""
        extensions = {
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".sh",
            ".go",
            ".rs",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".cs",
            ".rb",
            ".php",
        }
        files = []
        exclude_dirs = {
            ".git",
            "__pycache__",
            "node_modules",
            "venv",
            ".venv",
            "build",
            "dist",
            ".pytest_cache",
            "test",
            "tests",
        }

        for path in Path(folder_path).rglob("*"):
            if path.is_file() and path.suffix in extensions:
                if not any(excluded in path.parts for excluded in exclude_dirs):
                    files.append(path)
        return sorted(files)

    def detect_or_select_framework(self, folder_path):
        """Auto-detect or let user select test framework."""
        self.header()
        print(f"{Colors.CYAN}🧪 {TEXTS[self.language]['framework']}{Colors.RESET}\n")

        detected = []
        if (
            (folder_path / "pytest.ini").exists()
            or (folder_path / "pyproject.toml").exists()
            or (folder_path / "setup.py").exists()
        ):
            detected.append("pytest")
        if (folder_path / "package.json").exists():
            detected.append("jest")
        if (folder_path / "Cargo.toml").exists():
            detected.append("rust")
        if (folder_path / "go.mod").exists():
            detected.append("go")

        frameworks = (
            ["Auto-detect"]
            + detected
            + ["pytest", "unittest", "jest", "mocha", "go", "rust", "manual"]
        )

        result = self.select_single_interactive(
            TEXTS[self.language]["select_framework"], frameworks
        )

        if result is None or result == 0:
            return detected[0] if detected else "pytest"
        return frameworks[result]

    def select_ai_model(self):
        """Select AI model for test generation."""
        self.header()
        print(f"{Colors.CYAN}🤖 {TEXTS[self.language]['select_model']}{Colors.RESET}\n")

        default_model = self.runner.config.get("DEFAULT_MODEL", "qwen3.5:0.8b")
        print(f"  [1] Default: {default_model}")
        print(f"  [2] {TEXTS[self.language]['custom_model']}")
        print(f"  [V] {TEXTS[self.language]['back']}\n")

        choice = input(f"{Colors.YELLOW}>> {Colors.RESET}").strip().lower()

        if choice == "v":
            return default_model
        elif choice == "1":
            return default_model
        elif choice == "2":
            print(f"\n{Colors.CYAN}{TEXTS[self.language]['enter_model']}{Colors.RESET}")
            model = input(f"{Colors.YELLOW}>> {Colors.RESET}").strip()
            return model if model else default_model
        return default_model

    def select_test_category(self):
        """Select test category."""
        categories = [
            "core",
            "integration",
            "paths",
            "network",
            "ui",
            "assets",
            "performance",
            "custom",
        ]

        result = self.select_single_interactive(
            TEXTS[self.language]["select_category"], categories
        )

        if result is None:
            return "core"
        return categories[result]

    def generate_tests_with_ai(
        self, files, base_path, framework, model, save_path, category
    ):
        """Generate tests using AI."""
        self.header()
        print(
            f"{Colors.CYAN}🤖 {TEXTS[self.language]['generating_tests']}{Colors.RESET}\n"
        )

        if not self.runner.ollama.available:
            print(f"{Colors.RED}Ollama not available{Colors.RESET}")
            input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")
            return

        file_contents = []
        for f in files:
            try:
                with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                    # Aumentamos a 15000 para capturar archivos completos o secciones muy grandes
                    content = fp.read(15000)
                    rel_path = str(f.relative_to(base_path))
                    file_contents.append(f"File: {rel_path}\n---\n{content}\n---\n")
            except:
                pass

        prompt = f"""You are an expert QA Engineer. Generate a comprehensive, professional test suite.

Framework: {framework}
Category: {category}
Language: {Path(files[0]).suffix}

SOURCE CODE TO ANALYZE:
{"".join(file_contents)}

INSTRUCTIONS:
1. Analyze the logic, data structures, and potential failure points.
2. Generate tests covering:
   - Happy paths (standard functionality)
   - Edge cases (nulls, empty strings, limits)
   - Error handling (expected exceptions/errors)
3. Ensure high code quality:
   - Use descriptive test names
   - Include clear comments explaining the 'why' of each test
   - Use the most appropriate assertions for {framework}
   - Follow industry best practices for {framework}
4. Structure:
   - Include necessary imports
   - Use classes for organization if idiomatic to {framework}
   - Add setup/teardown if required

IMPORTANT: Return ONLY the raw code. No markdown code blocks, no preamble, no conversational text.
"""

        print(f"{Colors.CYAN}Using model: {model}{Colors.RESET}")

        result = self.runner.ollama.generate(model, prompt, temperature=0.3)

        if result:
            test_dir = save_path / category
            test_dir.mkdir(parents=True, exist_ok=True)

            test_file = (
                test_dir
                / f"test_generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            )

            with open(test_file, "w") as f:
                # Inyectar logo en el código generado
                f.write(f"\"\"\"\n{decode_ascii(ASCII_RAINBOW)}\n\"\"\"\n\n")
                f.write(f"""# Generated Tests - {category}
# Framework: {framework}
# Generated: {datetime.now()}
# Model: {model}
# Files analyzed: {len(files)}

{result}
""")

            print(
                f"{Colors.GREEN}✓ {TEXTS[self.language]['saving_tests']} {test_file}{Colors.RESET}"
            )
            input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")
        else:
            print(f"{Colors.RED}✗ Test generation failed{Colors.RESET}")
            input(f"{Colors.YELLOW}{TEXTS[self.language]['enter']}{Colors.RESET}")


# #rainbowtechnology.xyz #You're not supposed to see this! #i-love-you

# ════════════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════════════


def main():
    show_xyz()

    # #xyz-rainbow #rainbow.xyz

    # Detectar el directorio base del proyecto
    script_path = Path(__file__).resolve()
    test_folder = script_path.parent  # scripts/
    project_root = test_folder.parent  # xyz-test-runner/

    # Si hay una carpeta tests/ o test/ en project_root, usar project_root
    if (project_root / "tests").exists() or (project_root / "test").exists():
        base_dir = project_root
    else:
        base_dir = test_folder.parent  # Por defecto, subir un nivel

    # Prioridad de archivos de configuración
    config_candidates = [
        base_dir / "config",
        base_dir / "tests" / "config",
        base_dir / "test" / "config",
        test_folder / "config"
    ]
    
    config_path = None
    for candidate in config_candidates:
        if candidate.exists():
            config_path = candidate
            break
            
    if not config_path:
        config_path = test_folder / "config"

    config = TestConfig(str(config_path))
    runner = TestRunner(str(base_dir), config, config.get("LANGUAGE", "en"))
    menu = Menu(runner)

    # Si el usuario no ha especificado el idioma, preguntar
    if "LANGUAGE" not in config.values:
        menu.select_language()
    
    runner.language = menu.language
    runner.discover_categories_and_tests()
    runner.select_all()
    menu.main_menu()


if __name__ == "__main__":
    main()

# ════════════════════════════════════════════════════════════════════════════════════
# FINAL DEL SCRIPT - FIRMA DE CALIDAD XYZ
# #xyz-rainbow #rainbowtechnology.xyz #i-love-you #You're not supposed to see this!
# ════════════════════════════════════════════════════════════════════════════════════

# ▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
# ▐                                                                                          ▌
# ▐                                                 _           _                            ▌
# ▐    __  __  _   _   ____          _ __    __ _  (_)  _ __   | |__     ___   __      __    ▌
# ▐    \ \/ / | | | | |_  /  _____  | '__|  / _` | | | | '_ \  | '_ \   / _ \  \ \ /\ / /    ▌
# ▐     >  <  | |_| |  / /  |_____| | |    | (_| | | | | | | | | |_) | | (_) |  \ V  V /     ▌
# ▐    /_/\\_\\  \\__, | /___|         |_|     \\__,_| |_| |_| |_|_.__/   \\___/    _/\\_/       ▌
# ▐            |___/                                                                         ▌
# ▐                                                                                          ▌
# ▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌

# ┌──────────────────────────────────────────────────────────────────────┐
# │                                                                      │
# │                                    _       _                         │
# │     __  ___   _ ____     _ __ __ _(_)_ __ | |__   _____      __      │
# │     \\ \\/ / | | |_  /____| '__/ _` | | '_ \\| '_ \\ / _ \\ \\ /\\ / /      │
# │      >  <| |_| |/ /_____| | | (_| | | | | | |_) | (_) \\ V  V /       │
# │     /_/\\_\\\\__, /___|    |_|  \\__,_|_|_| |_|_.__/ \\___/ \\_/\_/        │
# │           |___/                                                      │
# │                                                                      │
# └──────────────────────────────────────────────────────────────────────┘
