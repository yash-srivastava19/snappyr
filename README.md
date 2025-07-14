# Snappyr - Setup Projects Blazingly Fast 🚀

[![PyPI](https://img.shields.io/pypi/v/snappyr)](https://pypi.org/project/snappyr/)
[![Python](https://img.shields.io/pypi/pyversions/snappyr)](https://pypi.org/project/snappyr/)
[![License](https://img.shields.io/github/license/yash-srivastava19/snappyr)](https://github.com/yash-srivastava19/snappyr)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[PyPI](https://pypi.org/project/snappyr/) | [Repository](https://github.com/yash-srivastava19/snappyr)

## Introduction

Snappyr is a modern Python project scaffolding tool that sets up professional Python projects with industry-standard tooling in seconds. Instead of manually configuring the same development environment repeatedly, Snappyr creates a complete, production-ready project structure with modern tools like **uv**, **ruff**, **mypy**, and **pre-commit hooks**.

## ✨ Features

Snappyr creates projects with professional development practices out of the box:

### 🏗️ **Modern Project Structure**
```
project_name/
├── src/
│   ├── main.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── scripts/
├── docs/
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml        # Modern Python packaging
├── .pre-commit-config.yaml
├── .gitignore
├── .env
├── LICENSE
└── README.md
```

### ⚡ **Modern Dependency Management with UV**
- Uses [uv](https://github.com/astral-sh/uv) instead of pip/poetry for ultra-fast dependency management
- Automatic virtual environment creation and management
- Lock file generation for reproducible builds

### 🧹 **Code Quality & Linting**
- **Ruff**: Lightning-fast Python linter and formatter (replaces black, flake8, isort)
- **Mypy**: Comprehensive type checking with strict configuration
- **Pre-commit hooks**: Automated code quality checks on every commit

### 🧪 **Testing & Coverage**
- **Pytest** with coverage reporting
- Pre-configured test structure
- GitHub Actions CI/CD workflow

### 📦 **Professional Package Setup**
- Modern `pyproject.toml` configuration
- Support for multiple Python versions (3.11+)
- Configurable license types (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause)
- Package mode for library development

## 🚀 Installation

### Via pip (Recommended)
```bash
pip install snappyr
```

### Via uv (if you have uv installed)
```bash
uv tool install snappyr
```

## 📖 Usage

### Basic Usage
```bash
# Create a new project
snappyr my_awesome_project

# Or with options
snappyr my_project --python-version 3.12 --license Apache-2.0
```

### Advanced Options
```bash
snappyr my_project \
  --is_package \              # Set up as a Python package
  --python-version 3.12 \     # Target Python version
  --license MIT \             # Choose license type
  --no-git \                  # Skip Git initialization
  --no-precommit              # Skip pre-commit setup
```

### Available Options
- `--is_package`: Configure project as a Python package with proper structure
- `--python-version`: Target Python version (default: 3.11)
- `--license`: License type - MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, None (default: MIT)
- `--no-git`: Skip Git repository initialization
- `--no-precommit`: Skip pre-commit hooks setup
- `--version`: Show version information

## 🔧 What Gets Created

### Development Tools Configuration
- **pyproject.toml**: Modern Python packaging with comprehensive tool configuration
- **Ruff**: Configured with sensible defaults for linting and formatting
- **Mypy**: Strict type checking configuration
- **Pytest**: Testing framework with coverage reporting
- **Pre-commit**: Automated quality checks including ruff, mypy, and security scanning

### GitHub Actions CI
- Multi-Python version testing (3.11, 3.12)
- Automated linting, formatting, and type checking
- Test coverage reporting
- Codecov integration

### Professional Files
- Comprehensive `.gitignore` for Python projects
- License file with proper copyright notice
- Professional README template with badges
- Environment file template

## 🏃‍♂️ Quick Start After Project Creation

```bash
cd your_project

# Install dependencies
uv sync

# Run the project
uv run python src/main.py

# Run tests
uv run pytest

# Code quality checks
uv run ruff check .          # Lint code
uv run ruff format .         # Format code  
uv run mypy .                # Type checking

# Set up pre-commit (if not skipped)
uv run pre-commit install
uv run pre-commit run --all-files
```

## 🛠️ Development Workflow

The generated projects support a modern development workflow:

1. **Write code** in `src/`
2. **Write tests** in `tests/`
3. **Quality checks** run automatically via pre-commit
4. **CI/CD** runs on GitHub Actions
5. **Dependencies** managed with uv

## 📋 Prerequisites

Snappyr requires these tools to be installed:
- **Python 3.11+**
- **uv**: `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **git**: For version control (optional but recommended)

## 🎯 Why Choose Snappyr?

### **Speed**: Get from idea to coding in seconds
### **Modern**: Uses the latest Python tooling and best practices  
### **Professional**: Creates production-ready project structure
### **Opinionated**: Sensible defaults that work for most projects
### **Extensible**: Easy to customize the generated structure

## 🆚 Comparison with Other Tools

| Feature | Snappyr | Cookiecutter | Poetry new |
|---------|---------|--------------|------------|
| Modern tooling (uv, ruff) | ✅ | ❌ | ❌ |
| Pre-commit hooks | ✅ | Depends | ❌ |
| CI/CD setup | ✅ | Depends | ❌ |
| Type checking setup | ✅ | Depends | ❌ |
| Zero configuration | ✅ | ❌ | ❌ |
| Speed | ⚡ | 🐌 | 🚀 |

## 🤝 Contributing

Contributions are welcome! This project uses the same modern tooling it creates:

```bash
# Clone and set up development environment
git clone https://github.com/yash-srivastava19/snappyr
cd snappyr
uv sync --all-extras

# Run tests
uv run pytest

# Quality checks  
uv run ruff check .
uv run mypy .
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [uv](https://github.com/astral-sh/uv) for blazing-fast Python package management
- [ruff](https://github.com/astral-sh/ruff) for lightning-fast linting and formatting
- [mypy](https://github.com/python/mypy) for comprehensive type checking
