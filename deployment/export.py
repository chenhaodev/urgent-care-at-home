"""
Export Optimized Agent for Production Deployment.

Packages the optimized agent with metadata and deployment instructions.
"""

import json
from pathlib import Path
from datetime import datetime


def export_production_agent():
    """
    Package optimized agent with all dependencies.

    Outputs:
    - package_info.json: Metadata about the deployment package
    - Verification that compiled agent and protocols exist
    """
    # Create package metadata
    package = {
        "version": "1.0.0",
        "model": "deepseek-chat",
        "framework": "dspy",
        "created_at": datetime.now().isoformat(),
        "protocols_count": 225,
        "optimization": {
            "method": "BootstrapFewShot",
            "training_cases": 32,
            "target_red_flag_accuracy": "100%",
        },
        "files": {
            "compiled_agent": "deployment/compiled_triage_agent.json",
            "protocols": "protocols/protocols.json",
            "test_cases": "dataset/cases.json",
        },
    }

    # Verify required files exist
    required_files = [
        Path("deployment/compiled_triage_agent.json"),
        Path("protocols/protocols.json"),
        Path("dataset/cases.json"),
    ]

    missing_files = [f for f in required_files if not f.exists()]

    if missing_files:
        print("Missing required files:")
        for f in missing_files:
            print(f"  - {f}")
        print("\nRun these commands first:")
        print("  1. uv run python protocols/parser.py")
        print("  2. uv run python dataset/generator.py")
        print("  3. uv run python optimization/compile.py")
        return False

    # Save package metadata
    deployment_dir = Path("deployment")
    deployment_dir.mkdir(exist_ok=True)

    with open(deployment_dir / "package_info.json", "w") as f:
        json.dump(package, f, indent=2)

    print("=" * 60)
    print("Production Package Ready")
    print("=" * 60)
    print("\nPackage contents:")
    for name, path in package["files"].items():
        file_path = Path(path)
        size = file_path.stat().st_size if file_path.exists() else 0
        print(f"  - {name}: {path} ({size:,} bytes)")

    print(f"\nMetadata: deployment/package_info.json")
    print(f"Version: {package['version']}")
    print(f"Framework: {package['framework']} + {package['model']}")

    print("\nDeployment Instructions:")
    print("1. Copy all files in package['files'] to production server")
    print("2. Install dependencies: uv add dspy-ai pydantic python-dotenv")
    print("3. Set DEEPSEEK_API_KEY in production .env")
    print("4. Load agent: agent.triage_module.load('deployment/compiled_triage_agent.json')")

    return True


if __name__ == "__main__":
    success = export_production_agent()
    exit(0 if success else 1)
