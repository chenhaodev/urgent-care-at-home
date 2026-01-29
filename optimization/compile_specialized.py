"""
Compile Specialized Nurse Agents.

Optimizes triage agents for specific nurse roles using domain-targeted training data.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import dspy
from agent.triage_agent import STCCTriageAgent
from agent.settings import get_deepseek_config
from dataset.nurse_roles import NurseRole, get_specialization
from dataset.specialized_generator import generate_specialized_dataset
from dataset.schema import PatientCase
from optimization.optimizer import get_optimizer
from optimization.metric import protocol_adherence_metric
import json


def compile_specialized_agent(
    role: NurseRole,
    force_regenerate_data: bool = False,
) -> str:
    """
    Compile a specialized triage agent for a specific nurse role.

    Args:
        role: The nurse role specialization
        force_regenerate_data: Whether to regenerate training data

    Returns:
        Path to the compiled agent JSON file
    """
    specialization = get_specialization(role)

    print("=" * 70)
    print(f"Compiling Specialized Agent: {specialization.display_name}")
    print("=" * 70)
    print(f"Description: {specialization.description}")
    print(f"Focus areas: {', '.join(specialization.focus_symptoms[:5])}...")
    print()

    # Step 1: Load or generate specialized training data
    dataset_path = Path(__file__).parent.parent / "dataset" / f"cases_{role.value}.json"

    if not dataset_path.exists() or force_regenerate_data:
        print("Generating specialized training dataset...")
        generate_specialized_dataset(role)
    else:
        print(f"Using existing dataset: {dataset_path}")

    # Load training cases
    with dataset_path.open("r", encoding="utf-8") as f:
        cases_data = json.load(f)

    trainset = [PatientCase(**case) for case in cases_data]

    print(f"\nTraining set: {len(trainset)} specialized cases")
    distribution = {}
    for case in trainset:
        distribution[case.triage_level] = distribution.get(case.triage_level, 0) + 1

    print("Distribution:")
    for level, count in sorted(distribution.items()):
        print(f"  {level}: {count} cases")

    # Step 2: Initialize agent
    print("\nInitializing triage agent...")
    config = get_deepseek_config()
    dspy.configure(lm=config.lm)

    agent = STCCTriageAgent()

    # Step 3: Optimize with BootstrapFewShot
    print(f"\nOptimizing for {specialization.display_name}...")
    print("This may take 5-10 minutes...")

    teleprompter = get_optimizer()

    # Compile with domain-specific training data
    compiled_agent = teleprompter.compile(
        agent.triage_module,
        trainset=trainset,
        valset=trainset[:len(trainset) // 2],  # Use first half for validation
    )

    # Step 4: Save compiled agent
    output_path = (
        Path(__file__).parent.parent
        / "deployment"
        / f"compiled_{role.value}_agent.json"
    )
    output_path.parent.mkdir(exist_ok=True, parents=True)

    compiled_agent.save(str(output_path))

    print(f"\n✓ Compiled {specialization.display_name} agent saved to:")
    print(f"  {output_path}")

    return str(output_path)


def compile_all_specializations():
    """Compile agents for all nurse specializations."""
    print("\n" + "=" * 70)
    print("SPECIALIZED NURSE AGENT COMPILER")
    print("=" * 70)

    roles = [
        NurseRole.CHF_NURSE,
        NurseRole.PREOP_NURSE,
        NurseRole.ED_NURSE,
        NurseRole.PEDIATRIC_NURSE,
        NurseRole.RESPIRATORY_NURSE,
    ]

    compiled_agents = {}

    for role in roles:
        try:
            output_path = compile_specialized_agent(role, force_regenerate_data=False)
            compiled_agents[role.value] = output_path
            print()
        except Exception as e:
            print(f"\n✗ Error compiling {role.value}: {e}")
            print()

    # Summary
    print("=" * 70)
    print("COMPILATION SUMMARY")
    print("=" * 70)

    for role_name, path in compiled_agents.items():
        spec = get_specialization(NurseRole(role_name))
        print(f"✓ {spec.display_name:20s} → {Path(path).name}")

    print(f"\nTotal: {len(compiled_agents)} specialized agents compiled")
    print("=" * 70)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compile specialized nurse agents")
    parser.add_argument(
        "--role",
        type=str,
        choices=[r.value for r in NurseRole],
        help="Specific role to compile (default: all)",
    )
    parser.add_argument(
        "--regenerate-data",
        action="store_true",
        help="Force regenerate training data",
    )

    args = parser.parse_args()

    if args.role:
        # Compile single role
        compile_specialized_agent(
            NurseRole(args.role),
            force_regenerate_data=args.regenerate_data,
        )
    else:
        # Compile all roles
        compile_all_specializations()
