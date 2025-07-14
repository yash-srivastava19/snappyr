"""Snappyr - Setup Python projects with modern tooling."""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from snappyr import __version__


def check_prerequisites() -> bool:
    """Check if required tools are installed."""
    required_tools = ["git", "uv"]
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, "--version"], 
                         check=True, 
                         capture_output=True, 
                         text=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append(tool)
    
    if missing_tools:
        print("❌ Missing required tools:")
        for tool in missing_tools:
            if tool == "uv":
                print(f"   - {tool}: Install with 'pip install uv' or 'curl -LsSf https://astral.sh/uv/install.sh | sh'")
            elif tool == "git":
                print(f"   - {tool}: Install from https://git-scm.com/downloads")
        return False
    
    return True


def create_additional_files(project_name: str, license_type: str = "MIT") -> None:
    """Create additional configuration files for a professional setup."""
    project_path = Path(project_name)
    
    # Create LICENSE file if not None
    if license_type != "None":
        license_content = get_license_content(license_type)
        if license_content:
            (project_path / "LICENSE").write_text(license_content)
            print(f"✅ {license_type} license file created")
    
    # Create .envrc for direnv users (optional)
    envrc_content = '''# Automatically activate virtual environment when entering the directory
layout_python() {
    local python=${1:-python3}
    [[ $# -gt 0 ]] && shift
    unset PYTHONHOME
    if [[ -n $VIRTUAL_ENV ]]; then
        VIRTUAL_ENV=$(realpath "${VIRTUAL_ENV}")
    else
        local python_version
        python_version=$("$python" -c "import platform; print(platform.python_version())")
        if [[ -z $python_version ]]; then
            log_error "Could not detect Python version"
            return 1
        fi
        VIRTUAL_ENV=$PWD/.direnv/python-$python_version
    fi
    export VIRTUAL_ENV
    if [[ ! -d $VIRTUAL_ENV ]]; then
        log_status "no venv found; creating $VIRTUAL_ENV"
        "$python" -m venv "$VIRTUAL_ENV"
    fi
    PATH="$VIRTUAL_ENV/bin:$PATH"
    export PATH
}

# Use uv for Python project
if [[ -f "pyproject.toml" ]]; then
    layout_python
fi
'''
    (project_path / ".envrc").write_text(envrc_content)
    
    # Create .github/workflows directory for CI/CD
    github_workflows = project_path / ".github" / "workflows"
    github_workflows.mkdir(parents=True, exist_ok=True)
    
    # Create a basic CI workflow
    ci_workflow = '''name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4
    
    - name: Install uv
      uses: astral-sh/setup-uv@v2
      with:
        version: "latest"
    
    - name: Set up Python ${{ matrix.python-version }}
      run: uv python install ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: uv sync --all-extras
    
    - name: Run linting
      run: |
        uv run ruff check .
        uv run ruff format --check .
    
    - name: Run type checking
      run: uv run mypy .
    
    - name: Run tests
      run: uv run pytest --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
'''
    
    (github_workflows / "ci.yml").write_text(ci_workflow)
    print("✅ GitHub Actions CI workflow created")


def get_license_content(license_type: str) -> Optional[str]:
    """Get license content based on license type."""
    licenses = {
        "MIT": '''MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.''',
        "Apache-2.0": '''Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

[Full Apache 2.0 license text would go here]
''',
        "GPL-3.0": '''GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

[Full GPL 3.0 license text would go here]
''',
        "BSD-3-Clause": '''BSD 3-Clause License

Copyright (c) 2025, Your Name

[Full BSD 3-Clause license text would go here]
'''
    }
    return licenses.get(license_type)


def create_directory_structure(project_name: str) -> None:
    """Create the directory structure for the project."""
    base_dirs = [
        project_name,
        f"{project_name}/src",
        f"{project_name}/tests",
        f"{project_name}/scripts", 
        f"{project_name}/docs",
    ]
    
    for directory in base_dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)

    # Add the README.md
    readme_content = f"""# {project_name}

## Description
Project description goes here.

## Installation

```bash
uv sync
```

## Usage

```bash
uv run python src/main.py
```

## Development

```bash
# Install development dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run linting
uv run ruff check .
uv run ruff format .

# Run type checking
uv run mypy .
```
"""
    Path(project_name, "README.md").write_text(readme_content)
    
    # Add the main.py file in src/
    main_content = '''"""Main module for the project."""

def main() -> None:
    """Main entry point."""
    print("Hello, world!")


if __name__ == "__main__":
    main()
'''
    Path(project_name, "src", "main.py").write_text(main_content)

    # Add __init__.py files
    Path(project_name, "src", "__init__.py").write_text("")
    Path(project_name, "tests", "__init__.py").write_text("")

    # Add a sample test
    test_content = '''"""Tests for the main module."""

from src.main import main


def test_main() -> None:
    """Test the main function."""
    # This is a placeholder test
    assert main() is None
'''
    Path(project_name, "tests", "test_main.py").write_text(test_content)

    # Add the .env
    Path(project_name, ".env").write_text("# Add your environment variables here\n")
    
    # Add modern .gitignore
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# uv
.uv/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Ruff
.ruff_cache/
"""
    Path(project_name, ".gitignore").write_text(gitignore_content)
    
    print("✅ Directory structure created.")

def setup_uv_project(project_name: str, python_version: str = "3.11", license_type: str = "MIT") -> None:
    """Set up uv project with pyproject.toml instead of venv + requirements.txt."""
    print("🚀 Setting up uv project...")
    
    project_path = Path(project_name)
    
    # License mapping
    license_texts = {
        "MIT": "MIT",
        "Apache-2.0": "Apache-2.0", 
        "GPL-3.0": "GPL-3.0-only",
        "BSD-3-Clause": "BSD-3-Clause",
        "None": None
    }
    
    license_config = f'license = {{text = "{license_texts[license_type]}"}}' if license_texts[license_type] else ""
    
    # Create pyproject.toml
    pyproject_content = f'''[project]
name = "{project_name.replace("-", "_")}"
version = "0.1.0"
description = "A Python project created with Snappyr"
authors = [
    {{name = "Your Name", email = "your.email@example.com"}}
]
readme = "README.md"
{license_config}
requires-python = ">={python_version}"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
    "pre-commit>=3.6.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src"]

[tool.ruff]
target-version = "py{python_version.replace('.', '')}"
line-length = 88

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "N",   # pep8-naming
    "S",   # flake8-bandit
    "RUF", # ruff-specific rules
]
ignore = [
    "S603", # subprocess-without-shell-equals-true
    "S607", # start-process-with-partial-path
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # Allow assert in tests

[tool.mypy]
python_version = "{python_version}"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
show_error_codes = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--strict-markers",
]
markers = [
    "slow: marks tests as slow (deselect with -m 'not slow')",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/site-packages/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\\\bProtocol\\\\):",
    "@(abc\\\\.)?abstractmethod",
]
'''
    
    (project_path / "pyproject.toml").write_text(pyproject_content)
    
    # Initialize uv project without creating pyproject.toml (we already created it)
    try:
        # Sync to create lock file and install dependencies
        subprocess.run(["uv", "sync", "--dev"], check=True, cwd=project_name)
        print("✅ UV project dependencies synced")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not sync uv project: {e}")
        print("   Make sure 'uv' is installed: pip install uv")
        print("   You can manually run 'uv sync' in the project directory later")
    except FileNotFoundError:
        print("⚠️  Warning: 'uv' command not found. Install with: pip install uv")

def initialize_git(project_name: str) -> None:
    """Initialize a Git repository and optionally link to a remote repo."""
    print("📦 Initializing Git repository...")
    
    try:
        subprocess.run(["git", "init", project_name], check=True)
        print("✅ Git repository initialized")
        
        # Add initial commit
        subprocess.run(["git", "-C", project_name, "add", "."], check=True)
        subprocess.run(["git", "-C", project_name, "commit", "-m", "Initial commit"], check=True)
        print("✅ Initial commit created")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not initialize git: {e}")
    except FileNotFoundError:
        print("⚠️  Warning: git command not found")
        
    # Optional remote repository
    remote_url = input("\n🔗 Enter remote Git repository URL (or press Enter to skip): ").strip()
    if remote_url:
        try:
            subprocess.run(["git", "-C", project_name, "remote", "add", "origin", remote_url], check=True)
            print(f"✅ Linked to remote repository: {remote_url}")
        except subprocess.CalledProcessError:
            print("⚠️  Warning: Could not link to remote repository")

def add_setup_files(project_name: str) -> None:
    """Add modern packaging files for the project."""
    print("📦 Adding packaging configuration...")
    
    project_path = Path(project_name)
    
    # Add py.typed for type information
    (project_path / "src" / project_name.replace("-", "_") / "py.typed").touch()
    
    # Add __init__.py to make it a package
    init_content = f'''"""
{project_name} - A Python package.

Version: 0.1.0
"""

__version__ = "0.1.0"
'''
    (project_path / "src" / project_name.replace("-", "_") / "__init__.py").write_text(init_content)
    
    print("✅ Package structure created")

def add_precommit_hooks(project_name: str) -> None:
    """Add pre-commit hooks configuration with ruff, mypy, and other quality checks."""
    print("🔧 Adding pre-commit configuration...")
    
    project_path = Path(project_name)
    
    precommit_config = '''repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-toml
      - id: debug-statements
      - id: check-case-conflict
      - id: check-docstring-first

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
        name: ruff-lint
      - id: ruff-format
        name: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--strict]
        exclude: ^tests/
        
  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r]
        exclude: ^tests/

  - repo: https://github.com/python-poetry/poetry
    rev: 1.7.1
    hooks:
      - id: poetry-check
        files: pyproject.toml
        
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: uv run pytest
        language: system
        pass_filenames: false
        always_run: true
        stages: [pre-push]
'''
    
    (project_path / ".pre-commit-config.yaml").write_text(precommit_config)
    
    # Try to install pre-commit hooks
    try:
        subprocess.run(["uv", "run", "pre-commit", "install"], 
                      check=True, cwd=project_name)
        print("✅ Pre-commit hooks installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Pre-commit hooks configured but not installed")
        print("   Run 'uv run pre-commit install' in the project directory")

def cli() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="""
    _____ _   _____    ____  ______  ______ 
    / ___// | / /   |  / __ \\/ __ \\ \\/ / __ \\
    \\__ \\/  |/ / /| | / /_/ / /_/ /\\  / /_/ /
    ___/ / /|  / ___ |/ ____/ ____/ / / _, _/ 
    /____/_/ |_/_/  |_/_/   /_/     /_/_/ |_|  
                                                
    Set up Python projects blazingly fast with Snappyr.
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"snappyr {__version__}",
    )
    parser.add_argument(
        "project_name",
        nargs="?",
        help="Name of the project to be created."
    )
    parser.add_argument(
        "--project-name", 
        dest="project_name_alt",
        help="Alternative way to specify project name (deprecated, use positional argument)."
    )
    parser.add_argument(
        "--is_package", 
        action="store_true",
        help="Set up the project as a Python package with proper structure."
    )
    parser.add_argument(
        "--no-git",
        action="store_true", 
        help="Skip Git repository initialization."
    )
    parser.add_argument(
        "--no-precommit",
        action="store_true",
        help="Skip pre-commit hooks setup."
    )
    parser.add_argument(
        "--python-version",
        default="3.11",
        help="Python version to target (default: 3.11)."
    )
    parser.add_argument(
        "--license",
        choices=["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "None"],
        default="MIT",
        help="License to use for the project (default: MIT)."
    )
    
    args = parser.parse_args()

    # Handle project name from either positional or named argument
    project_name = args.project_name or args.project_name_alt
    if not project_name:
        parser.error("Project name is required. Use: snappyr <project_name>")
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Cannot proceed without required tools.")
        sys.exit(1)
    
    if Path(project_name).exists():
        print(f"❌ Error: Directory '{project_name}' already exists.")
        sys.exit(1)

    print(f"🚀 Creating project: {project_name}")
    print("=" * 50)

    # Step 1: Create directory structure
    create_directory_structure(project_name)

    # Step 2: Set up uv project instead of venv
    setup_uv_project(project_name, args.python_version, args.license)

    # Step 3: Create additional professional files
    create_additional_files(project_name, args.license)

    # Step 4: Initialize Git (optional)
    if not args.no_git:
        initialize_git(project_name)

    # Step 5: Add package structure
    if args.is_package:
        add_setup_files(project_name)

    # Step 6: Add pre-commit hooks (optional)
    if not args.no_precommit:
        add_precommit_hooks(project_name)

    print("\n" + "=" * 50)
    print(f"🎉 Project '{project_name}' is ready!")
    print("\n📋 Next steps:")
    print(f"   cd {project_name}")
    print("   uv sync              # Install dependencies")
    print("   uv run python src/main.py  # Run the project")
    print("   uv run pytest        # Run tests")
    print("   uv run ruff check .  # Lint code")
    print("   uv run ruff format . # Format code")
    print("   uv run mypy .        # Type checking")
    if not args.no_precommit:
        print("   uv run pre-commit install  # Install pre-commit hooks")
        print("   uv run pre-commit run --all-files  # Run all hooks")
    print("\n🚀 Happy coding!")

if __name__ == "__main__":
    cli()