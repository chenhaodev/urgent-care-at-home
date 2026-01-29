#!/usr/bin/env python3
"""
Compile and save optimized triage agent.

This script runs the BootstrapFewShot optimization and saves
the compiled program for production deployment.
"""

from pathlib import Path
from optimization.optimizer import optimize_triage_agent


def main():
    """Run optimization and save compiled program."""

    print("=" * 60)
    print("STCC Triage Agent - DSPy Optimization & Compilation")
    print("=" * 60)

    try:
        # Run optimization
        print("\nStep 1: Running BootstrapFewShot optimization...")
        optimized_agent = optimize_triage_agent(
            max_bootstrapped_demos=8, max_labeled_demos=4, max_rounds=1
        )

        # Create deployment directory
        deployment_dir = Path("deployment")
        deployment_dir.mkdir(exist_ok=True)

        # Save compiled program
        output_path = deployment_dir / "compiled_triage_agent.json"
        print(f"\nStep 2: Saving compiled agent to {output_path}...")

        optimized_agent.triage_module.save(str(output_path))

        print("\n" + "=" * 60)
        print("✓ Optimization Complete!")
        print("=" * 60)
        print(f"\nOptimized agent saved to: {output_path}")
        print("\nTo use in production:")
        print("  from agent.triage_agent import STCCTriageAgent")
        print("  agent = STCCTriageAgent()")
        print(f"  agent.triage_module.load('{output_path}')")
        print("\nNext steps:")
        print("  1. Run edge case validation: uv run python validation/edge_cases.py")
        print("  2. Run unit tests: uv run pytest validation/test_agent.py -v")

    except Exception as e:
        print(f"\n✗ Optimization failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure dataset exists: uv run python dataset/generator.py")
        print("2. Ensure protocols parsed: uv run python protocols/parser.py")
        print("3. Check .env file has DEEPSEEK_API_KEY")
        print("4. Verify DeepSeek API key is valid")
        raise


if __name__ == "__main__":
    main()
