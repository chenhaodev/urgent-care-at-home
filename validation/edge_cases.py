"""
Edge Case Validation - Red-Flag Stress Test.

Tests agent on critical red-flag symptoms to ensure 100% emergency detection.
"""

import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.triage_agent import STCCTriageAgent
from dataset.schema import PatientCase


# Critical red-flag test cases
# These MUST trigger Emergency triage 100% of the time
RED_FLAG_CASES = [
    PatientCase(
        case_id=101,
        protocol_category="Chest Pain",
        patient_age=58,
        symptoms="Crushing chest pain radiating to jaw and left arm, profuse cold sweat, nausea, feeling like about to die",
        medical_history="Smoker for 30 years, high cholesterol, family history of heart disease",
        triage_level="emergency",
        rationale="Classic acute myocardial infarction presentation - immediate ambulance required",
    ),
    PatientCase(
        case_id=102,
        protocol_category="Breathing Problems",
        patient_age=6,
        symptoms="Severe difficulty breathing, blue lips and fingernails, cannot speak at all, gasping",
        medical_history="Asthma",
        triage_level="emergency",
        rationale="Severe respiratory failure with cyanosis in child - life-threatening emergency",
    ),
    PatientCase(
        case_id=103,
        protocol_category="Abdominal Pain",
        patient_age=70,
        symptoms="Sudden severe abdominal pain, vomiting large amounts of bright red blood, very pale, dizzy",
        medical_history="Takes warfarin for atrial fibrillation",
        triage_level="emergency",
        rationale="Major GI bleeding in anticoagulated patient - hemorrhagic shock risk",
    ),
    PatientCase(
        case_id=104,
        protocol_category="Chest Pain",
        patient_age=65,
        symptoms="Chest pain for 2 hours not relieved by rest or nitroglycerin, shortness of breath, sweating",
        medical_history="Previous heart attack, diabetes, hypertension",
        triage_level="emergency",
        rationale="Unstable angina/MI in high-risk patient - immediate intervention needed",
    ),
    PatientCase(
        case_id=105,
        protocol_category="Breathing Problems",
        patient_age=50,
        symptoms="Sudden severe shortness of breath, sharp chest pain worse with breathing, recent long flight",
        medical_history="Recent hip surgery 10 days ago",
        triage_level="emergency",
        rationale="High suspicion for pulmonary embolism with major risk factors",
    ),
    PatientCase(
        case_id=106,
        protocol_category="Abdominal Pain",
        patient_age=32,
        symptoms="Sudden severe lower abdominal and shoulder pain, missed period 7 weeks, lightheaded, pale",
        medical_history="IUD removed 3 months ago, sexually active",
        triage_level="emergency",
        rationale="Ruptured ectopic pregnancy with hemorrhage - surgical emergency",
    ),
    PatientCase(
        case_id=107,
        protocol_category="Breathing Problems",
        patient_age=75,
        symptoms="Coughing up pink frothy sputum, severe shortness of breath even at rest, cannot lie flat",
        medical_history="Congestive heart failure, recent medication changes",
        triage_level="emergency",
        rationale="Acute pulmonary edema from heart failure - needs immediate treatment",
    ),
    PatientCase(
        case_id=108,
        protocol_category="Chest Pain",
        patient_age=52,
        symptoms="Severe chest pain, heart racing over 180 bpm, ICD device has shocked 3 times in last hour",
        medical_history="Cardiomyopathy with implanted defibrillator",
        triage_level="emergency",
        rationale="Ventricular tachycardia with multiple ICD firings - life-threatening arrhythmia",
    ),
    PatientCase(
        case_id=109,
        protocol_category="Breathing Problems",
        patient_age=4,
        symptoms="High fever 40°C, drooling, cannot swallow, sitting forward to breathe, high-pitched breathing sounds",
        medical_history="Sore throat started yesterday",
        triage_level="emergency",
        rationale="Epiglottitis or severe airway obstruction in child - airway emergency",
    ),
    PatientCase(
        case_id=110,
        protocol_category="Abdominal Pain",
        patient_age=82,
        symptoms="Severe tearing abdominal pain radiating to back, fainted briefly, blood pressure very low",
        medical_history="Hypertension, smoker, known abdominal aortic aneurysm",
        triage_level="emergency",
        rationale="Ruptured abdominal aortic aneurysm - immediately life-threatening",
    ),
]


def test_red_flag_detection(agent: STCCTriageAgent) -> dict:
    """
    Test agent on red-flag cases - must achieve 100% accuracy.

    Args:
        agent: Initialized STCCTriageAgent

    Returns:
        dict: Test results with pass/fail status
    """
    results = {"total_cases": len(RED_FLAG_CASES), "correct": 0, "failures": []}

    print(f"\nTesting {len(RED_FLAG_CASES)} red-flag cases...")
    print("-" * 60)

    for i, case in enumerate(RED_FLAG_CASES, 1):
        try:
            prediction = agent.triage(case.symptoms)

            # Check if emergency was detected
            pred_level = prediction.triage_level.lower().strip()
            is_correct = pred_level == "emergency"

            if is_correct:
                results["correct"] += 1
                status = "✓ PASS"
            else:
                status = "✗ FAIL"
                results["failures"].append(
                    {
                        "case_id": case.case_id,
                        "symptoms": case.symptoms,
                        "expected": "emergency",
                        "got": prediction.triage_level,
                        "reasoning": prediction.clinical_justification,
                    }
                )

            print(f"Case {i}/{len(RED_FLAG_CASES)}: {status} - {case.protocol_category}")

        except Exception as e:
            print(f"Case {i}/{len(RED_FLAG_CASES)}: ✗ ERROR - {e}")
            results["failures"].append(
                {
                    "case_id": case.case_id,
                    "symptoms": case.symptoms,
                    "expected": "emergency",
                    "got": "ERROR",
                    "reasoning": str(e),
                }
            )

    results["accuracy"] = results["correct"] / results["total_cases"]
    results["passed"] = results["accuracy"] == 1.0

    return results


def run_edge_case_validation():
    """Run complete edge case test suite."""
    print("=" * 60)
    print("Red-Flag Stress Test - Emergency Detection Validation")
    print("=" * 60)

    try:
        # Load agent (with or without compiled optimization)
        print("\nInitializing triage agent...")
        agent = STCCTriageAgent()

        # Check if compiled version exists
        compiled_path = Path("deployment/compiled_triage_agent.json")
        if compiled_path.exists():
            print(f"Loading optimized agent from {compiled_path}")
            agent.triage_module.load(str(compiled_path))
        else:
            print("Using base agent (not optimized)")
            print("Run 'uv run python optimization/compile.py' to optimize first")

        # Test red flags
        results = test_red_flag_detection(agent)

        # Print results
        print("\n" + "=" * 60)
        print("Results Summary")
        print("=" * 60)
        print(f"Total Cases:  {results['total_cases']}")
        print(f"Correct:      {results['correct']}")
        print(f"Failed:       {len(results['failures'])}")
        print(f"Accuracy:     {results['accuracy']:.1%}")
        print(f"Status:       {'PASS ✓' if results['passed'] else 'FAIL ✗'}")

        if results["failures"]:
            print("\n" + "=" * 60)
            print("Failed Cases (CRITICAL)")
            print("=" * 60)
            for failure in results["failures"]:
                print(f"\nCase #{failure['case_id']}:")
                print(f"  Symptoms: {failure['symptoms'][:80]}...")
                print(f"  Expected: {failure['expected']}")
                print(f"  Got:      {failure['got']}")
                print(f"  Reason:   {failure['reasoning'][:100]}...")

        # Save report
        report_path = Path("validation/edge_case_report.json")
        report_path.parent.mkdir(exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\nReport saved to: {report_path}")

        # Return status code
        return 0 if results["passed"] else 1

    except Exception as e:
        print(f"\n✗ Validation failed with error: {e}")
        print("\nMake sure:")
        print("1. Protocols parsed: uv run python protocols/parser.py")
        print("2. DeepSeek API key in .env file")
        raise


if __name__ == "__main__":
    import sys

    exit_code = run_edge_case_validation()
    sys.exit(exit_code)
