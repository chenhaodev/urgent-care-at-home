"""
Gold-Standard Dataset Generator.

Generates synthetic patient cases for training and validation.
"""

from pathlib import Path
import json
from typing import List
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dataset.schema import PatientCase


def generate_gold_standard_cases() -> List[PatientCase]:
    """
    Generate diverse patient cases covering:
    - All urgency levels (emergency, urgent, moderate, home_care)
    - Red-flag symptoms (chest pain, breathing difficulty, etc.)
    - Edge cases and multi-symptom scenarios
    - Different age groups (pediatric, adult, elderly)

    Returns:
        List of 30+ PatientCase objects with balanced distribution
    """
    cases = [
        # ============ EMERGENCY CASES (Red Flags) ============
        PatientCase(
            case_id=1,
            protocol_category="Chest Pain",
            patient_age=55,
            symptoms="Severe crushing chest pain radiating to left arm and jaw, shortness of breath, cold sweaty skin, nausea",
            medical_history="History of high blood pressure, smoker for 30 years, high cholesterol",
            triage_level="emergency",
            rationale="Classic signs of acute myocardial infarction - requires immediate ambulance",
        ),
        PatientCase(
            case_id=2,
            protocol_category="Breathing Problems",
            patient_age=8,
            symptoms="Severe wheezing, unable to speak full sentences, bluish lips and fingernails, gasping for air",
            medical_history="Known asthma, inhaler not providing relief",
            triage_level="emergency",
            rationale="Severe respiratory distress with cyanosis - call ambulance immediately for respiratory failure",
        ),
        PatientCase(
            case_id=3,
            protocol_category="Abdominal Pain",
            patient_age=70,
            symptoms="Sudden onset severe abdominal pain, vomiting bright red blood, very pale skin, dizziness when standing",
            medical_history="Takes blood thinners (warfarin) for atrial fibrillation",
            triage_level="emergency",
            rationale="Possible GI bleeding in anticoagulated patient - life-threatening hemorrhage risk",
        ),
        PatientCase(
            case_id=4,
            protocol_category="Chest Pain",
            patient_age=62,
            symptoms="Persistent chest tightness for 30 minutes, pain radiating to neck and shoulder, cold sweat, feeling of impending doom",
            medical_history="Diabetes type 2, previous heart attack 5 years ago",
            triage_level="emergency",
            rationale="Possible acute coronary syndrome in high-risk patient with cardiac history",
        ),
        PatientCase(
            case_id=5,
            protocol_category="Breathing Problems",
            patient_age=45,
            symptoms="Sudden severe difficulty breathing, chest pain that worsens with deep breath, recent long flight from Asia",
            medical_history="Recent knee surgery 2 weeks ago, takes birth control pills",
            triage_level="emergency",
            rationale="Possible pulmonary embolism with risk factors (recent surgery, immobility, oral contraceptives)",
        ),
        PatientCase(
            case_id=6,
            protocol_category="Abdominal Pain",
            patient_age=28,
            symptoms="Sudden severe lower abdominal pain, missed period by 6 weeks, shoulder pain, lightheaded",
            medical_history="No significant past history, sexually active",
            triage_level="emergency",
            rationale="Possible ruptured ectopic pregnancy - life-threatening internal bleeding",
        ),
        PatientCase(
            case_id=7,
            protocol_category="Breathing Problems",
            patient_age=3,
            symptoms="Sudden difficulty breathing, high-pitched sound when breathing in, drooling, unable to swallow, leaning forward",
            medical_history="Sore throat for 1 day, fever 39.5°C",
            triage_level="emergency",
            rationale="Possible epiglottitis or severe airway obstruction in child - medical emergency",
        ),
        PatientCase(
            case_id=8,
            protocol_category="Chest Pain",
            patient_age=58,
            symptoms="Severe chest pain, heart palpitations, implanted defibrillator has shocked multiple times in last hour",
            medical_history="Heart failure, implanted cardiac defibrillator",
            triage_level="emergency",
            rationale="Multiple ICD firings indicate life-threatening arrhythmia - immediate care needed",
        ),
        # ============ URGENT CASES ============
        PatientCase(
            case_id=9,
            protocol_category="Abdominal Pain",
            patient_age=67,
            symptoms="Severe abdominal pain for 6 hours, vomiting, no bowel movement for 3 days, abdomen feels hard and bloated",
            medical_history="Previous abdominal surgery for colon cancer, diabetes",
            triage_level="urgent",
            rationale="Possible bowel obstruction in high-risk patient - needs emergency care within hours",
        ),
        PatientCase(
            case_id=10,
            protocol_category="Chest Pain",
            patient_age=72,
            symptoms="New onset chest pain that comes and goes, shortness of breath when walking",
            medical_history="High blood pressure, high cholesterol, age over 60",
            triage_level="urgent",
            rationale="New cardiac symptoms in elderly with risk factors - needs urgent evaluation",
        ),
        PatientCase(
            case_id=11,
            protocol_category="Abdominal Pain",
            patient_age=35,
            symptoms="Sudden severe right lower abdominal pain, fever 38.5°C, nausea, loss of appetite",
            medical_history="No significant medical history",
            triage_level="urgent",
            rationale="Classic presentation of appendicitis - needs urgent surgical evaluation",
        ),
        PatientCase(
            case_id=12,
            protocol_category="Breathing Problems",
            patient_age=65,
            symptoms="Progressively worsening shortness of breath over 2 days, coughing pink frothy sputum, swollen ankles",
            medical_history="Congestive heart failure, hypertension",
            triage_level="urgent",
            rationale="Acute heart failure exacerbation with pulmonary edema - needs urgent care",
        ),
        PatientCase(
            case_id=13,
            protocol_category="Breathing Problems",
            patient_age=42,
            symptoms="Fever 39°C, severe cough with yellow-green sputum, chest pain when breathing, shortness of breath",
            medical_history="Diabetes, weakened immune system",
            triage_level="urgent",
            rationale="Severe pneumonia in immunocompromised patient - needs urgent antibiotic treatment",
        ),
        PatientCase(
            case_id=14,
            protocol_category="Abdominal Pain",
            patient_age=55,
            symptoms="Persistent severe upper abdominal pain radiating to back, nausea, vomiting",
            medical_history="Heavy alcohol use, previous pancreatitis",
            triage_level="urgent",
            rationale="Possible acute pancreatitis - potentially life-threatening, needs urgent care",
        ),
        PatientCase(
            case_id=15,
            protocol_category="Chest Pain",
            patient_age=48,
            symptoms="Chest pain that started 3 hours ago, pain score 7/10, associated with nausea",
            medical_history="Smoker, father had heart attack at age 50",
            triage_level="urgent",
            rationale="Chest pain with cardiac risk factors - rule out acute coronary syndrome urgently",
        ),
        PatientCase(
            case_id=16,
            protocol_category="Breathing Problems",
            patient_age=12,
            symptoms="Moderate wheezing, speaks in short phrases, peak flow 60% of normal, used inhaler with minimal relief",
            medical_history="Asthma",
            triage_level="urgent",
            rationale="Moderate asthma exacerbation with poor response to treatment - needs urgent care",
        ),
        # ============ MODERATE URGENCY CASES ============
        PatientCase(
            case_id=17,
            protocol_category="Abdominal Pain",
            patient_age=32,
            symptoms="Right lower abdominal pain for 8 hours, mild nausea, low-grade fever 37.8°C",
            medical_history="No significant medical history",
            triage_level="moderate",
            rationale="Possible early appendicitis - needs evaluation within 2-4 hours",
        ),
        PatientCase(
            case_id=18,
            protocol_category="Chest Pain",
            patient_age=25,
            symptoms="Sharp chest pain when taking deep breath, recent coughing for 3 days, pain worsens with movement",
            medical_history="Upper respiratory infection diagnosed 3 days ago",
            triage_level="moderate",
            rationale="Likely pleurisy from respiratory infection - needs evaluation but not emergency",
        ),
        PatientCase(
            case_id=19,
            protocol_category="Abdominal Pain",
            patient_age=45,
            symptoms="Upper abdominal pain after meals for 2 days, bloating, some nausea",
            medical_history="History of gallstones",
            triage_level="moderate",
            rationale="Possible biliary colic - needs medical evaluation within hours",
        ),
        PatientCase(
            case_id=20,
            protocol_category="Breathing Problems",
            patient_age=38,
            symptoms="Mild shortness of breath, productive cough for 3 days, fever 38°C, chest discomfort",
            medical_history="No chronic conditions",
            triage_level="moderate",
            rationale="Likely bronchitis or mild pneumonia - needs evaluation and possible antibiotics",
        ),
        PatientCase(
            case_id=21,
            protocol_category="Abdominal Pain",
            patient_age=29,
            symptoms="Lower abdominal cramping pain, diarrhea for 2 days, low-grade fever 37.5°C",
            medical_history="Recent restaurant meal",
            triage_level="moderate",
            rationale="Possible food poisoning or gastroenteritis - monitor for dehydration",
        ),
        PatientCase(
            case_id=22,
            protocol_category="Breathing Problems",
            patient_age=18,
            symptoms="Mild wheezing, peak flow 70% of normal, slight shortness of breath during exercise",
            medical_history="Asthma, usually well controlled",
            triage_level="moderate",
            rationale="Mild asthma exacerbation - needs evaluation but not urgent emergency",
        ),
        PatientCase(
            case_id=23,
            protocol_category="Chest Pain",
            patient_age=40,
            symptoms="Burning chest pain after eating spicy food, worse when lying down, no shortness of breath",
            medical_history="History of acid reflux",
            triage_level="moderate",
            rationale="Likely GERD flare-up - needs evaluation if symptoms persist or worsen",
        ),
        # ============ HOME CARE CASES ============
        PatientCase(
            case_id=24,
            protocol_category="Abdominal Pain",
            patient_age=28,
            symptoms="Mild cramping abdominal pain after eating spicy food, no fever, no vomiting",
            medical_history="Occasional heartburn, otherwise healthy",
            triage_level="home_care",
            rationale="Likely dietary indiscretion - home care with antacids, follow up if worsens",
        ),
        PatientCase(
            case_id=25,
            protocol_category="Chest Pain",
            patient_age=22,
            symptoms="Brief sharp chest pain near ribs after lifting heavy boxes, pain only with movement and touch",
            medical_history="No medical problems, exercises regularly",
            triage_level="home_care",
            rationale="Musculoskeletal chest pain from strain - rest, ice, over-the-counter pain relief",
        ),
        PatientCase(
            case_id=26,
            protocol_category="Abdominal Pain",
            patient_age=35,
            symptoms="Mild upper abdominal discomfort, bloating after large meal, no fever or vomiting",
            medical_history="No significant history",
            triage_level="home_care",
            rationale="Overeating/indigestion - home care with antacids and smaller meals",
        ),
        PatientCase(
            case_id=27,
            protocol_category="Breathing Problems",
            patient_age=30,
            symptoms="Mild shortness of breath during anxiety attack, rapid breathing, tingling in fingers",
            medical_history="Anxiety disorder, recent stressful life events",
            triage_level="home_care",
            rationale="Hyperventilation from anxiety - breathing exercises, follow up with therapist",
        ),
        PatientCase(
            case_id=28,
            protocol_category="Abdominal Pain",
            patient_age=50,
            symptoms="Mild abdominal cramping, gas, bloating after eating dairy products",
            medical_history="Known lactose intolerance, usually avoids dairy",
            triage_level="home_care",
            rationale="Lactose intolerance symptoms - avoid dairy, use lactase supplements",
        ),
        PatientCase(
            case_id=29,
            protocol_category="Chest Pain",
            patient_age=19,
            symptoms="Occasional chest tightness during panic attacks, resolves when anxiety subsides",
            medical_history="Diagnosed anxiety disorder, no cardiac issues",
            triage_level="home_care",
            rationale="Anxiety-related chest discomfort - continue anxiety management, follow up with therapist",
        ),
        PatientCase(
            case_id=30,
            protocol_category="Breathing Problems",
            patient_age=26,
            symptoms="Mild nasal congestion, slight cough, no fever, otherwise feeling well",
            medical_history="No chronic conditions",
            triage_level="home_care",
            rationale="Common cold - rest, fluids, over-the-counter symptom relief",
        ),
        # Additional edge cases
        PatientCase(
            case_id=31,
            protocol_category="Abdominal Pain",
            patient_age=15,
            symptoms="Mild lower abdominal cramping, started today, no fever",
            medical_history="Female, regular menstrual cycles",
            triage_level="home_care",
            rationale="Likely menstrual cramps - heat therapy, over-the-counter pain relief",
        ),
        PatientCase(
            case_id=32,
            protocol_category="Chest Pain",
            patient_age=68,
            symptoms="New chest discomfort that improves with rest but returns with exertion, no shortness of breath at rest",
            medical_history="Diabetes, high blood pressure",
            triage_level="urgent",
            rationale="Possible angina in high-risk patient - needs urgent cardiac evaluation",
        ),
    ]

    # Save to JSON
    output_path = Path("dataset/cases.json")
    output_path.parent.mkdir(exist_ok=True, parents=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            [c.model_dump() for c in cases],
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Generated {len(cases)} patient cases, saved to {output_path}")
    return cases


if __name__ == "__main__":
    cases = generate_gold_standard_cases()

    # Print distribution
    from collections import Counter

    distribution = Counter(c.triage_level for c in cases)
    print("\nCase Distribution:")
    for level, count in sorted(distribution.items()):
        print(f"  {level}: {count} cases")
