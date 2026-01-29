#!/usr/bin/env python3
"""
Verify Repository Setup.

Checks that all required files and configurations are in place
before pushing to GitHub.
"""

from pathlib import Path
import sys


def check_file_exists(path: Path, description: str) -> bool:
    """Check if a file exists and report."""
    if path.exists():
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path} - NOT FOUND")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("STCC Triage Agent - Repository Verification")
    print("=" * 60)

    checks = []

    # Documentation
    print("\n📚 Documentation Files:")
    checks.append(check_file_exists(Path("README.md"), "README"))
    checks.append(check_file_exists(Path("LICENSE"), "License"))
    checks.append(check_file_exists(Path("CONTRIBUTING.md"), "Contributing Guide"))
    checks.append(check_file_exists(Path("CHANGELOG.md"), "Changelog"))
    checks.append(check_file_exists(Path("SECURITY.md"), "Security Policy"))

    # Configuration
    print("\n⚙️ Configuration Files:")
    checks.append(check_file_exists(Path("pyproject.toml"), "Project Config"))
    checks.append(check_file_exists(Path("requirements.txt"), "Requirements"))
    checks.append(check_file_exists(Path(".gitignore"), "Git Ignore"))
    checks.append(check_file_exists(Path(".env.example"), "Env Template"))


    # Core Modules
    print("\n🐍 Core Python Modules:")
    modules = [
        "agent/triage_agent.py",
        "agent/signature.py",
        "agent/settings.py",
        "protocols/parser.py",
        "dataset/generator.py",
        "dataset/schema.py",
        "optimization/metric.py",
        "optimization/optimizer.py",
        "optimization/compile.py",
        "validation/test_agent.py",
        "validation/edge_cases.py",
        "deployment/api.py",
        "deployment/export.py",
        "examples/basic_triage.py",
    ]

    for module in modules:
        checks.append(check_file_exists(Path(module), f"Module: {module}"))

    # Summary
    print("\n" + "=" * 60)
    passed = sum(checks)
    total = len(checks)
    print(f"Results: {passed}/{total} checks passed")

    if passed == total:
        print("✅ Repository is ready for GitHub!")
        print("\nNext steps:")
        print("  1. git init")
        print("  2. git add .")
        print('  3. git commit -m "Initial commit: STCC Triage Agent v1.0.0"')
        print("  4. git remote add origin <your-repo-url>")
        print("  5. git push -u origin main")
        return 0
    else:
        print(f"❌ {total - passed} checks failed. Fix issues before pushing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
