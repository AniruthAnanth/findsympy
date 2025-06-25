#!/usr/bin/env python3
"""
Development helper script for FINDSYM package.
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and print its description."""
    print(f"\n=== {description} ===")
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Error: Command failed with return code {result.returncode}")
        return False
    return True

def clean():
    """Clean build artifacts."""
    commands = [
        "rm -rf build/ dist/ *.egg-info/",
        "find . -name __pycache__ -type d -exec rm -rf {} +",
        "find . -name '*.pyc' -delete"
    ]
    
    for cmd in commands:
        run_command(cmd, f"Cleaning: {cmd}")

def format_code():
    """Format code using black and isort."""
    commands = [
        "black findsym/ examples/ test_*.py",
        "isort findsym/ examples/ test_*.py"
    ]
    
    for cmd in commands:
        run_command(cmd, f"Formatting: {cmd}")

def lint():
    """Run linting checks."""
    commands = [
        "flake8 findsym/ examples/ test_*.py",
        "black --check findsym/ examples/ test_*.py",
        "isort --check-only findsym/ examples/ test_*.py"
    ]
    
    success = True
    for cmd in commands:
        if not run_command(cmd, f"Linting: {cmd}"):
            success = False
    
    return success

def test():
    """Run tests."""
    return run_command("pytest", "Running tests")

def build():
    """Build the package."""
    clean()
    return run_command("python -m build", "Building package")

def build_check():
    """Check the built package."""
    return run_command("twine check dist/*", "Checking built package")

def upload():
    """Upload to PyPI."""
    print("\n=== Uploading to PyPI ===")
    print("Note: You'll need to enter your PyPI credentials")
    return run_command("twine upload dist/*", "Uploading to PyPI")

def install_dev():
    """Install in development mode."""
    return run_command("pip install -e .", "Installing in development mode")

def help_text():
    """Show help text."""
    print("""
FINDSYM Development Helper

Available commands:
  clean          - Remove build artifacts and cache files
  format         - Format code using black and isort
  lint           - Run linting checks (flake8, black, isort)
  test           - Run test suite
  build          - Build the package
  build-check    - Check the built package
  install-dev    - Install in development mode
  upload         - Upload to PyPI
  help           - Show this help

Complete release workflow:
  1. python dev.py clean
  2. python dev.py format
  3. python dev.py lint
  4. python dev.py test
  5. python dev.py build
  6. python dev.py build-check
  7. python dev.py upload
""")

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        help_text()
        return
    
    command = sys.argv[1]
    
    commands = {
        'clean': clean,
        'format': format_code,
        'lint': lint,
        'test': test,
        'build': build,
        'build-check': build_check,
        'upload': upload,
        'install-dev': install_dev,
        'help': help_text
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        help_text()

if __name__ == "__main__":
    main()
