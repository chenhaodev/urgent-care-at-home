"""
STCC Triage Agent with DSPy ChainOfThought.

Main triage agent using DeepSeek for medical reasoning.
"""

import json
from pathlib import Path
from typing import List

try:
    import dspy
    from dspy import ChainOfThought
except ImportError:
    raise ImportError("dspy-ai package not installed. Run: uv add dspy-ai")

from .signature import TriageSignature
from .settings import get_deepseek_config


class STCCTriageAgent:
    """
    Medical triage agent using DSPy ChainOfThought with DeepSeek.

    Features:
    - Chain-of-thought reasoning for transparent decision-making
    - STCC protocol context enhancement
    - DeepSeek-powered reasoning engine
    - Structured output with clinical justification
    """

    def __init__(self, protocols_path: str = "protocols/protocols.json"):
        """
        Initialize triage agent.

        Args:
            protocols_path: Path to digitized STCC protocols JSON file
        """
        # Configure DeepSeek via DSPy
        config = get_deepseek_config()
        dspy.configure(lm=config.lm)

        # Load digitized protocols
        protocols_file = Path(protocols_path)
        if not protocols_file.exists():
            raise FileNotFoundError(
                f"Protocols file not found: {protocols_path}. "
                "Run: uv run python protocols/parser.py"
            )

        with open(protocols_path, "r", encoding="utf-8") as f:
            self.protocols = json.load(f)

        # Create ChainOfThought module
        # This adds step-by-step reasoning before final answer
        self.triage_module = ChainOfThought(TriageSignature)

        print(f"Triage agent initialized with {len(self.protocols)} protocols")

    def triage(self, symptoms: str) -> dspy.Prediction:
        """
        Perform triage on patient symptoms.

        Args:
            symptoms: Patient symptom description (natural language)

        Returns:
            DSPy Prediction with:
                - triage_level: Emergency/Urgent/Moderate/Home Care
                - clinical_justification: Reasoning
                - rationale: Chain-of-thought steps (added by ChainOfThought)
        """
        # Add protocol context to symptoms
        enhanced_prompt = self._add_protocol_context(symptoms)

        # Run ChainOfThought reasoning
        prediction = self.triage_module(symptoms=enhanced_prompt)

        return prediction

    def _add_protocol_context(self, symptoms: str) -> str:
        """
        Add relevant STCC protocol context to symptoms.

        CRITICAL: DSPy works best with context-rich inputs.
        Include protocol snippets matching symptom keywords.

        Args:
            symptoms: Raw patient symptom description

        Returns:
            Enhanced prompt with relevant protocol context
        """
        # Extract keywords from symptoms
        keywords = self._extract_keywords(symptoms)

        # Find matching protocols
        relevant_protocols = []
        for protocol in self.protocols:
            protocol_name_lower = protocol["protocol_name"].lower()
            if any(kw in protocol_name_lower for kw in keywords):
                relevant_protocols.append(protocol)

        # Build enhanced prompt
        context = f"Patient Presentation:\n{symptoms}\n\n"

        if relevant_protocols:
            context += "Relevant STCC Protocol Guidelines:\n"

            # Include top 2 most relevant protocols
            for protocol in relevant_protocols[:2]:
                context += f"\n{protocol['protocol_name']}:\n"

                # Add red flags (Section A - emergency)
                if protocol["sections"]:
                    emergency_section = protocol["sections"][0]
                    if emergency_section["urgency_level"] == "emergency":
                        context += "  Red Flags (Emergency - Call Ambulance):\n"
                        for condition in emergency_section["conditions"][:3]:
                            context += f"    - {condition}\n"

                # Add urgency levels and actions
                for section in protocol["sections"][:3]:  # Top 3 sections
                    level = section["urgency_level"]
                    action = section["action"]
                    context += f"  {level.title()}: {action}\n"
        else:
            # No specific protocol match - provide general guidance
            context += (
                "\nGeneral Triage Guidelines:\n"
                "- Emergency: Life-threatening symptoms requiring immediate ambulance\n"
                "- Urgent: Serious conditions needing emergency department care\n"
                "- Moderate: Needs medical evaluation within hours\n"
                "- Home Care: Can be managed with self-care at home\n"
            )

        return context

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract medical keywords for protocol matching.

        Args:
            text: Symptom description

        Returns:
            List of extracted keywords
        """
        keywords = []
        text_lower = text.lower()

        # Map common symptoms to protocol categories
        # This is simplified - in production, use medical NLP
        keyword_map = {
            "chest pain": ["chest", "pain", "cardiac", "heart"],
            "breathing": ["breathing", "respiratory", "asthma", "wheez", "dyspnea"],
            "abdominal": ["abdominal", "stomach", "belly", "abdomen"],
            "fever": ["fever", "temperature", "hot"],
            "headache": ["headache", "head pain"],
            "dizziness": ["dizzy", "lightheaded", "vertigo"],
            "nausea": ["nausea", "vomit", "nauseated"],
        }

        for category, terms in keyword_map.items():
            if any(term in text_lower for term in terms):
                keywords.append(category)

        return keywords if keywords else ["general"]


if __name__ == "__main__":
    # Test agent initialization
    try:
        agent = STCCTriageAgent()
        print("Agent initialized successfully!")

        # Test triage (requires DeepSeek API key in .env)
        test_symptoms = "55-year-old male with severe chest pain and shortness of breath"
        print(f"\nTest symptoms: {test_symptoms}")

        result = agent.triage(test_symptoms)
        print(f"Triage Level: {result.triage_level}")
        print(f"Justification: {result.clinical_justification}")

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("1. Run: uv run python protocols/parser.py")
        print("2. Create .env file with DEEPSEEK_API_KEY")
