<div align="center">
  <img src="assets/banner.svg" alt="XYZ Test Runner Banner" width="800">
</div>

---

## Features

- **Multi-format Reports**: MD, HTML, TXT, CSV
- **AI Integration**: Ollama-powered test interpretation
- **Auto-discovery**: Automatically finds test categories
- **Detailed Reports**: Full test output with error traces
- **Configurable**: Customize via `config` file
- **Portable**: Works with any Python project

---

## Installation

```bash
# Clone or copy to your project
cp -r xyz-test-runner /your/project/
cd /your/project/test

# Run
python3 scripts/xyz-test-runner.py
```

---

## Quick Start

```bash
cd your-project/test
python3 scripts/xyz-test-runner.py
```

### Menu Options

1. **Settings** - Configure AI, model, execution mode, GPU Protection, Xvfb
2. **Select Tests** - Choose categories and specific tests
3. **Run Tests** - Execute selected tests
4. **Results** - View results
5. **Generate Reports** - Export in multiple formats
6. **Create Tests with AI** - Generate tests using AI

### Xvfb (Headless Testing)

If tests crash your GNOME session, enable **Xvfb** in Settings. This runs tests on a virtual X server without affecting your desktop.

```bash
# Install (if not present)
sudo apt install xvfb

# Direct usage
xvfb-run -a python3 -m pytest test/tests/ -v
```

---

## Create Tests with AI

New in v2.0! Generate comprehensive test suites automatically using AI.

### How it Works

1. **Select Folder** - Choose project folder to analyze
2. **Select Files** - Multi-select source files using arrow keys + space
3. **Framework** - Auto-detect or choose manually (pytest, jest, go, rust, etc.)
4. **AI Model** - Select model for test generation (can differ from interpretation model)
5. **Save Location** - Choose where to save generated tests
6. **Category** - Select test category (core, integration, paths, network, ui, etc.)

### Supported Languages

- Python (.py)
- JavaScript/TypeScript (.js, .ts, .jsx, .tsx)
- Shell scripts (.sh)
- Go (.go)
- Rust (.rs)
- Java (.java)
- C/C++ (.c, .cpp, .h)
- And more...

### Auto-Detection

The runner automatically detects:
- pytest.ini / pyproject.toml → pytest
- package.json → jest
- Cargo.toml → rust
- go.mod → go

---

## Configuration

Edit the `config` file to customize:

```bash
# Language
LANGUAGE=en

# AI
USE_IA=false
DEFAULT_MODEL=qwen3.5:0.8b

# Report Detail
REPORT_DETAIL_LEVEL=full

# Export Formats
EXPORT_FORMATS=md,html,csv
```

---

## Project Structure

```
xyz-test-runner/
├── assets/                  # Official branding (CSS, SVG)
├── scripts/
│   └── xyz-test-runner.py   # Main runner
├── templates/
│   └── test_template.py    # Test template
├── tests/                   # Test categories
├── config                   # Configuration file
└── README.md               # This file
```

---

## Creating Tests

```bash
# Copy template
cp templates/test_template.py tests/your_category/your_test.py

# Edit your test
vim tests/your_category/your_test.py
```

### Test Structure

```python
class TestYourFeature:
    def setup_method(self):
        """Setup before each test"""
        pass
    
    def teardown_method(self):
        """Cleanup after each test"""
        pass
    
    def test_example(self):
        """Your test"""
        assert True
```

---

## Report Formats

### Markdown (.md)
Full report with tables, error traces, and statistics.

### HTML (.html)
Styled report with **XYZ - Rainbow Technology** official branding:
- Minimal Soft Grid design
- Futurist Cyberpunk aesthetics
- Glassmorphism & Neon accents
- Business Dark Branding

### CSV (.csv)
Export for Excel/analysis tools.

---

## Examples

### Run specific category
```
Select: 2 (Select Tests)
Select category: 1 (core)
Select tests: 1 (test_config.py)
Confirm: Enter
Execute: 3
```

### Generate AI interpretation
```
Settings: 1
Enable AI: 1 (toggle ON)
Select model: qwen3.5:0.8b
Generate: 5
```

---

## License

Personal Project - Non-commercial Use Only

Copyright © 2026 xyz-rainbow

---

## Contact

- **Email**: info@rainbowtechnology.xyz
- **GitHub**: github.com/xyz-rainbow

---

<div align="center">

**#xyz-rainbow #rainbowtechnology.xyz #i-love-you**

</div>
