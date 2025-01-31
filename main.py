import os
import subprocess
import sys

def create_directory_structure(project_name):
    """ Creates the directory structure for the project """
    
    # [PR]: Add more stuff. This is the directory structure I mostly go for.
    base_dirs = [
        f"{project_name}",
        f"{project_name}/src",
        f"{project_name}/tests",
        f"{project_name}/scripts",
        f"{project_name}/docs"
    ]
    for directory in base_dirs:
        os.makedirs(directory, exist_ok=True)

    # Add the README.md
    with open(os.path.join(project_name, "README.md"), "w") as f:
        f.write(f"# {project_name}\n\nProject Description")
    
    # Add the main.py file
    with open(os.path.join(project_name, "main.py"), "w") as f:
        f.write("# Main Python script\n\nif __name__ == '__main__':\n    print('Hello, world!')")

    # Add the requirements.txt
    with open(os.path.join(project_name, "requirements.txt"), "w") as f:
        f.write("# Add your dependencies here")
    
    # Add the .env
    with open(os.path.join(project_name, ".env"), "w") as f:
        f.write("# Add your secrets here")
    
    # Add the .gitignore
    with open(os.path.join(project_name, ".gitignore"), "w") as f:
        f.write("*.pyc\n__pycache__/\n.env\n.vscode/\n.idea/\n.DS_Store\nvenv/") # these are things we need to ignore ; works really well for now.
    
    print("Directory structure created.")

def setup_virtualenv(project_name):
    """ Sets up a virtual environment inside the project directory. This saves a lot of time."""
    
    print("Setting up virtual environment...")
    venv_path = os.path.join(project_name, "venv")
    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    
    print(f"Virtual environment created at: {venv_path}")
    print("To activate it, run:")
    
    if os.name == "nt":  # Windows
        print(f"{venv_path}\\Scripts\\activate")
    else:  # macOS/Linux
        print(f"source {venv_path}/bin/activate") # for different system, this might work.

def initialize_git(project_name):
    """ Initializes a Git repository and optionally links to a remote repo."""
    
    print("Initializing Git repository...")
    subprocess.run(["git", "init", project_name], check=True)
    remote_url = input("Enter remote Git repository URL (or press Enter to skip): ").strip()
    if remote_url:
        subprocess.run(["git", "-C", project_name, "remote", "add", "origin", remote_url], check=True)
        print(f"Linked to remote repository: {remote_url}")

def add_setup_files(project_name):
    """ Adds setup.py and setup.cfg for packaging the project. Will work when `is_package` is true"""

    print("Adding setup.py and setup.cfg for packaging...")
    with open(os.path.join(project_name, "setup.py"), "w") as f:
        f.write(f"""
    from setuptools import setup, find_packages

    setup(
        name="{project_name}",
        version="0.1.0",
        packages=find_packages(where="src"),
        package_dir={{"": "src"}},
        install_requires=[],  # Add dependencies here
    )
    """)
    with open(os.path.join(project_name, "setup.cfg"), "w") as f:
        f.write(f"""
    [metadata]
    name = {project_name}
    version = 0.1.0
    description = A Python project
    author = Your Name
    license = MIT
    [options]
    packages = find:
    package_dir =
        = src
    """)
    print("Setup files created.")

def add_precommit_hooks(project_name):
    """
    Adds a pre-commit hook configuration file.
    """
    print("Adding pre-commit configuration...")
    with open(os.path.join(project_name, ".pre-commit-config.yaml"), "w") as f:
        f.write("""
    repos:
    - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.4.0
        hooks:
        - id: trailing-whitespace
        - id: end-of-file-fixer
        - id: check-yaml
        - id: check-added-large-files
    """)
    print("Pre-commit configuration added. Install hooks with 'pre-commit install' after setup.")

def cli():
    pass

import argparse
parser = argparse.ArgumentParser(
    description=
"""
_____ _   _____    ____  ______  ______ 
/ ___// | / /   |  / __ \/ __ \ \/ / __ \
\__ \/  |/ / /| | / /_/ / /_/ /\  / /_/ /
___/ / /|  / ___ |/ ____/ ____/ / / _, _/ 
/____/_/ |_/_/  |_/_/   /_/     /_/_/ |_|  
                                            
Set up a Python projects blazingly fast with Snappyr.
"""
)

parser.add_argument("--project_name", help="Name of the project to be created.")
parser.add_argument("--is_package", help="Is the project a package.", default=False)
args = parser.parse_args()

project_name = args.project_name
if os.path.exists(project_name):
    print(f"Error: Directory '{project_name}' already exists.")
    exit()

# Step 1: Create directory structure
create_directory_structure(project_name)

# Step 2: Set up virtual environment
setup_virtualenv(project_name)

# Step 3: Initialize Git
initialize_git(project_name)

# Step 4: Add setup files
if args.is_package:
    add_setup_files(project_name)

# Step 5: Add pre-commit hooks (optional)
add_precommit_hooks(project_name)

print(f"\nProject '{project_name}' is ready! Happy coding!")

if __name__ == "__main__":
    cli() # dummy functions does our work.