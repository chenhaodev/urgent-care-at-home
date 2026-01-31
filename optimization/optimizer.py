"""
DSPy BootstrapFewShot Optimizer for Triage Agent.

Optimizes the triage agent using BootstrapFewShot with gold-standard dataset.
"""

import json
from pathlib import Path

try:
    import dspy
    from dspy.teleprompt import BootstrapFewShot
except ImportError:
    raise ImportError("dspy-ai package not installed. Run: uv add dspy-ai")

import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.triage_agent import STCCTriageAgent
from optimization.metric import combined_metric, protocol_adherence_metric


def get_optimizer(
    max_bootstrapped_demos: int = 8,
    max_labeled_demos: int = 4,
    max_rounds: int = 1,
    max_errors: int = 5,
) -> BootstrapFewShot:
    """
    Get configured BootstrapFewShot optimizer for specialized compilation.

    Args:
        max_bootstrapped_demos: Teacher-generated examples (default: 8)
        max_labeled_demos: Random samples from trainset (default: 4)
        max_rounds: Optimization rounds (default: 1)
        max_errors: Max errors allowed during bootstrapping (default: 5)

    Returns:
        Configured BootstrapFewShot teleprompter
    """
    return BootstrapFewShot(
        metric=protocol_adherence_metric,
        max_bootstrapped_demos=max_bootstrapped_demos,
        max_labeled_demos=max_labeled_demos,
        max_rounds=max_rounds,
        max_errors=max_errors,
    )


def optimize_triage_agent(
    max_bootstrapped_demos: int = 8,
    max_labeled_demos: int = 4,
    max_rounds: int = 1,
) -> STCCTriageAgent:
    """
    Optimize triage agent using BootstrapFewShot.

    Process:
    1. Load gold-standard training cases from dataset/cases.json
    2. Create BootstrapFewShot optimizer with combined metric
    3. Compile agent with optimized few-shot examples
    4. Return optimized agent

    Args:
        max_bootstrapped_demos: Teacher-generated examples (default: 8)
        max_labeled_demos: Random samples from trainset (default: 4)
        max_rounds: Optimization rounds (default: 1)

    Returns:
        Optimized STCCTriageAgent with compiled module
    """
    # Load training cases
    cases_path = Path("dataset/cases.json")
    if not cases_path.exists():
        raise FileNotFoundError(
            f"Cases file not found: {cases_path}. "
            "Run: uv run python dataset/specialized_generator.py"
        )

    with open(cases_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    print(f"Loaded {len(cases)} training cases")

    # Convert to DSPy format
    # PATTERN: DSPy expects trainset as list of dspy.Example objects
    trainset = []
    for case in cases:
        # Create example with inputs and expected outputs
        example = dspy.Example(
            symptoms=case["symptoms"], triage_level=case["triage_level"]
        ).with_inputs("symptoms")  # Mark 'symptoms' as the input field

        # Add the full case object for metric evaluation
        example.case = type("Case", (), case)()  # Convert dict to object

        trainset.append(example)

    print(f"Converted {len(trainset)} cases to DSPy format")

    # Create base agent
    agent = STCCTriageAgent()

    # Configure BootstrapFewShot optimizer
    print("\nConfiguring BootstrapFewShot optimizer...")
    optimizer = BootstrapFewShot(
        metric=combined_metric,
        max_bootstrapped_demos=max_bootstrapped_demos,
        max_labeled_demos=max_labeled_demos,
        max_rounds=max_rounds,
        max_errors=5,  # Allow some failures during bootstrapping
    )

    # Compile the agent
    # This generates optimized few-shot examples automatically
    print("\n" + "=" * 60)
    print("Starting optimization...")
    print("This may take 5-10 minutes depending on dataset size")
    print("=" * 60)

    compiled_module = optimizer.compile(
        student=agent.triage_module, trainset=trainset
    )

    # Update agent with compiled module
    agent.triage_module = compiled_module

    print("\n✓ Optimization complete!")
    return agent


if __name__ == "__main__":
    print("STCC Triage Agent - DSPy Optimization")
    print("=" * 60)

    try:
        # Run optimization
        optimized_agent = optimize_triage_agent(
            max_bootstrapped_demos=8, max_labeled_demos=4, max_rounds=1
        )

        print("\nOptimization successful!")
        print("Agent is now optimized with BootstrapFewShot examples")

    except Exception as e:
        print(f"\nError during optimization: {e}")
        print("\nMake sure:")
        print("1. Dataset exists: uv run python dataset/specialized_generator.py")
        print("2. Protocols parsed: uv run python protocols/parser.py")
        print("3. DeepSeek API key set in .env file")
        raise
