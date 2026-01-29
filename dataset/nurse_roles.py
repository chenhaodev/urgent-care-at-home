"""
Nurse Role Specializations.

Defines different nurse roles with their clinical focus areas
for domain-specific agent optimization.
"""

from enum import Enum
from typing import List
from pydantic import BaseModel


class NurseRole(str, Enum):
    """Specialized nurse role types."""

    # Cardiac specialization
    CHF_NURSE = "chf_nurse"  # Congestive Heart Failure
    CARDIAC_NURSE = "cardiac_nurse"  # General cardiac care

    # Surgical specialization
    PREOP_NURSE = "preop_nurse"  # Pre-operative assessment
    POSTOP_NURSE = "postop_nurse"  # Post-operative care

    # Emergency specialization
    ED_NURSE = "ed_nurse"  # Emergency Department
    TRAUMA_NURSE = "trauma_nurse"  # Trauma triage

    # Specialty areas
    PEDIATRIC_NURSE = "pediatric_nurse"  # Children
    ONCOLOGY_NURSE = "oncology_nurse"  # Cancer patients
    RESPIRATORY_NURSE = "respiratory_nurse"  # Respiratory issues
    NEURO_NURSE = "neuro_nurse"  # Neurological symptoms

    # General
    GENERAL_NURSE = "general_nurse"  # General triage


class NurseSpecialization(BaseModel):
    """Configuration for a specialized nurse role."""

    role: NurseRole
    display_name: str
    description: str
    focus_symptoms: List[str]  # Symptom keywords to prioritize
    focus_protocols: List[str]  # Protocol categories to focus on
    min_training_cases: int = 16  # Minimum cases needed for optimization


# Define specializations
NURSE_SPECIALIZATIONS = {
    NurseRole.CHF_NURSE: NurseSpecialization(
        role=NurseRole.CHF_NURSE,
        display_name="CHF Nurse",
        description="Congestive Heart Failure specialist - cardiac symptoms, fluid overload, dyspnea",
        focus_symptoms=[
            "chest pain",
            "shortness of breath",
            "dyspnea",
            "edema",
            "swelling",
            "heart palpitations",
            "fatigue",
            "orthopnea",
            "paroxysmal nocturnal dyspnea",
        ],
        focus_protocols=[
            "Chest Pain",
            "Shortness of Breath",
            "Swelling",
            "Heart Palpitations",
        ],
        min_training_cases=12,
    ),
    NurseRole.PREOP_NURSE: NurseSpecialization(
        role=NurseRole.PREOP_NURSE,
        display_name="PreOp Nurse",
        description="Pre-operative assessment specialist - surgical risk, medication review, clearance",
        focus_symptoms=[
            "surgical history",
            "medication review",
            "bleeding risk",
            "anesthesia concerns",
            "cardiac clearance",
            "infection",
            "fever",
        ],
        focus_protocols=[
            "Fever",
            "Chest Pain",
            "Bleeding",
            "Abdominal Pain",
        ],
        min_training_cases=12,
    ),
    NurseRole.ED_NURSE: NurseSpecialization(
        role=NurseRole.ED_NURSE,
        display_name="ED Nurse",
        description="Emergency Department specialist - acute trauma, emergencies, rapid assessment",
        focus_symptoms=[
            "trauma",
            "severe pain",
            "bleeding",
            "unconscious",
            "seizure",
            "chest pain",
            "difficulty breathing",
            "severe headache",
            "abdominal pain",
        ],
        focus_protocols=[
            "Chest Pain",
            "Head Injury",
            "Abdominal Pain",
            "Bleeding",
            "Breathing Problems",
            "Seizures",
        ],
        min_training_cases=16,
    ),
    NurseRole.PEDIATRIC_NURSE: NurseSpecialization(
        role=NurseRole.PEDIATRIC_NURSE,
        display_name="Pediatric Nurse",
        description="Child health specialist - infant/child symptoms, developmental concerns",
        focus_symptoms=[
            "fever in child",
            "infant crying",
            "rash",
            "vomiting",
            "diarrhea",
            "cough in child",
            "ear pain",
            "difficulty breathing in child",
        ],
        focus_protocols=[
            "Fever - Child",
            "Cough",
            "Vomiting",
            "Diarrhea",
            "Rash",
            "Ear Pain",
        ],
        min_training_cases=12,
    ),
    NurseRole.RESPIRATORY_NURSE: NurseSpecialization(
        role=NurseRole.RESPIRATORY_NURSE,
        display_name="Respiratory Nurse",
        description="Respiratory specialist - breathing issues, asthma, COPD, pneumonia",
        focus_symptoms=[
            "shortness of breath",
            "cough",
            "wheezing",
            "chest tightness",
            "difficulty breathing",
            "hypoxia",
            "respiratory distress",
        ],
        focus_protocols=[
            "Shortness of Breath",
            "Cough",
            "Chest Pain",
            "Breathing Problems",
        ],
        min_training_cases=12,
    ),
    NurseRole.GENERAL_NURSE: NurseSpecialization(
        role=NurseRole.GENERAL_NURSE,
        display_name="General Nurse",
        description="General triage nurse - broad coverage across all symptom types",
        focus_symptoms=[],  # No specific focus
        focus_protocols=[],  # All protocols
        min_training_cases=32,
    ),
}


def get_specialization(role: NurseRole) -> NurseSpecialization:
    """
    Get specialization configuration for a nurse role.

    Args:
        role: The nurse role

    Returns:
        NurseSpecialization configuration
    """
    return NURSE_SPECIALIZATIONS[role]


def list_available_roles() -> List[NurseRole]:
    """List all available nurse roles."""
    return list(NURSE_SPECIALIZATIONS.keys())
