"""
Comprehensive Unit Tests for STCC Triage Agent.

Tests all components: agent initialization, triage logic, metrics, and protocols.
"""

import pytest
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.triage_agent import STCCTriageAgent
from dataset.generator import generate_gold_standard_cases
from optimization.metric import (
    protocol_adherence_metric,
    red_flag_detection_metric,
    combined_metric,
)


@pytest.fixture
def agent():
    """Fixture: Initialized triage agent."""
    return STCCTriageAgent()


@pytest.fixture
def test_cases():
    """Fixture: Gold-standard test cases."""
    cases_path = Path("dataset/cases.json")
    if not cases_path.exists():
        # Generate if doesn't exist
        return generate_gold_standard_cases()

    with open(cases_path, "r", encoding="utf-8") as f:
        cases_data = json.load(f)

    # Convert to PatientCase objects
    from dataset.schema import PatientCase

    return [PatientCase(**case) for case in cases_data]


def test_agent_initialization(agent):
    """Test agent initializes correctly."""
    assert agent is not None
    assert agent.protocols is not None
    assert len(agent.protocols) > 200, "Should have 225+ STCC protocols"
    assert agent.triage_module is not None


def test_agent_has_protocols(agent):
    """Test that protocols are loaded and accessible."""
    assert isinstance(agent.protocols, list)
    if agent.protocols:
        # Check first protocol has expected structure
        protocol = agent.protocols[0]
        assert "protocol_name" in protocol
        assert "sections" in protocol


def test_emergency_detection_chest_pain(agent):
    """Test emergency symptom detection for chest pain."""
    result = agent.triage(
        "Patient is 60 years old with severe crushing chest pain "
        "radiating to left arm, shortness of breath, cold sweaty skin"
    )

    # Should detect as emergency
    assert result.triage_level.lower() == "emergency"


def test_emergency_detection_breathing(agent):
    """Test emergency detection for severe breathing problems."""
    result = agent.triage(
        "8-year-old child with severe wheezing, cannot speak, "
        "blue lips, inhaler not helping"
    )

    assert result.triage_level.lower() == "emergency"


def test_home_care_detection(agent):
    """Test home care triage for mild symptoms."""
    result = agent.triage(
        "Patient is 25 years old with mild headache after "
        "working on computer all day, no other symptoms, no fever"
    )

    # Should be home_care or moderate (mild symptoms)
    assert result.triage_level.lower() in ["home_care", "moderate", "home care"]


def test_protocol_context_enhancement(agent):
    """Test that protocol context is added to symptoms."""
    symptoms = "chest pain and shortness of breath"
    enhanced = agent._add_protocol_context(symptoms)

    # Should contain original symptoms
    assert symptoms in enhanced.lower()

    # Should contain protocol guidance
    assert "protocol" in enhanced.lower() or "triage" in enhanced.lower()


def test_keyword_extraction(agent):
    """Test medical keyword extraction."""
    keywords = agent._extract_keywords("Patient has chest pain and difficulty breathing")

    # Should extract relevant keywords
    assert len(keywords) > 0
    assert any(k in ["chest pain", "breathing"] for k in keywords)


# ============ Metric Tests ============


def test_metric_exact_match():
    """Test metric gives perfect score for exact match."""

    class MockGold:
        triage_level = "emergency"

    class MockPred:
        triage_level = "emergency"

    score = protocol_adherence_metric(MockGold(), MockPred())
    assert score == 1.0, "Exact match should score 1.0"


def test_metric_missed_emergency():
    """Test metric penalizes missed emergencies with zero score."""

    class MockGold:
        triage_level = "emergency"

    class MockPred:
        triage_level = "urgent"

    score = protocol_adherence_metric(MockGold(), MockPred())
    assert score == 0.0, "Missing emergency should score 0.0 (catastrophic)"


def test_metric_over_triage():
    """Test metric gives partial credit for over-triage (safer)."""

    class MockGold:
        triage_level = "urgent"

    class MockPred:
        triage_level = "emergency"

    score = protocol_adherence_metric(MockGold(), MockPred())
    assert score == 0.7, "Over-triage by 1 level should score 0.7"


def test_metric_under_triage():
    """Test metric penalizes under-triage."""

    class MockGold:
        triage_level = "urgent"

    class MockPred:
        triage_level = "moderate"

    score = protocol_adherence_metric(MockGold(), MockPred())
    assert score == 0.4, "Under-triage by 1 level should score 0.4"


def test_red_flag_metric_true():
    """Test red-flag detection returns True for correct emergency."""

    class MockGold:
        triage_level = "emergency"

    class MockPred:
        triage_level = "emergency"

    detected = red_flag_detection_metric(MockGold(), MockPred())
    assert detected is True


def test_red_flag_metric_false():
    """Test red-flag detection returns False for missed emergency."""

    class MockGold:
        triage_level = "emergency"

    class MockPred:
        triage_level = "urgent"

    detected = red_flag_detection_metric(MockGold(), MockPred())
    assert detected is False


def test_red_flag_metric_non_emergency():
    """Test red-flag metric returns True for non-emergency cases."""

    class MockGold:
        triage_level = "moderate"

    class MockPred:
        triage_level = "home_care"

    detected = red_flag_detection_metric(MockGold(), MockPred())
    assert detected is True, "Non-emergency cases should return True"


def test_combined_metric():
    """Test combined metric calculation."""

    class MockGold:
        triage_level = "emergency"

    class MockPred:
        triage_level = "emergency"

    score = combined_metric(MockGold(), MockPred())
    assert score == 1.0, "Perfect prediction should score 1.0"


# ============ Dataset Tests ============


def test_dataset_exists(test_cases):
    """Test that gold-standard dataset exists and has cases."""
    assert len(test_cases) >= 30, "Should have at least 30 test cases"


def test_dataset_distribution(test_cases):
    """Test that dataset has balanced distribution across triage levels."""
    from collections import Counter

    distribution = Counter(c.triage_level for c in test_cases)

    # Should have cases for all levels
    assert "emergency" in distribution
    assert "urgent" in distribution
    assert "moderate" in distribution or "home_care" in distribution

    # Should have at least 5 emergency cases for red-flag testing
    assert distribution["emergency"] >= 5


def test_emergency_cases_are_valid(test_cases):
    """Test that all emergency cases have appropriate symptoms."""
    emergency_cases = [c for c in test_cases if c.triage_level == "emergency"]

    for case in emergency_cases:
        # Should have symptoms
        assert len(case.symptoms) > 10
        # Should have rationale
        assert len(case.rationale) > 10
        # Age should be reasonable
        assert 0 < case.patient_age < 120


if __name__ == "__main__":
    # Run pytest
    pytest.main([__file__, "-v", "--tb=short"])
