"""
FastAPI Wrapper with Specialized Nurse Support.

Production API that supports loading different specialized nurse agents.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, Dict
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.triage_agent import STCCTriageAgent
from dataset.nurse_roles import NurseRole, get_specialization, NURSE_SPECIALIZATIONS

app = FastAPI(
    title="STCC Specialized Nurse Triage API",
    description="AI-powered medical triage with specialized nurse roles using DSPy and DeepSeek",
    version="2.0.0",
)

# Global storage for specialized agents
specialized_agents: Dict[str, STCCTriageAgent] = {}


@app.on_event("startup")
async def load_agents():
    """Load all available specialized nurse agents on startup."""
    global specialized_agents

    print("\n" + "=" * 70)
    print("Loading Specialized Nurse Agents...")
    print("=" * 70)

    deployment_dir = Path(__file__).parent

    # Try to load each specialized agent
    for role in NurseRole:
        try:
            agent = STCCTriageAgent()

            # Check for specialized compiled agent
            compiled_path = deployment_dir / f"compiled_{role.value}_agent.json"

            if compiled_path.exists():
                print(f"✓ Loading {role.value} from {compiled_path.name}")
                agent.triage_module.load(str(compiled_path))
                specialized_agents[role.value] = agent
            else:
                # Fall back to general agent for this role
                print(f"  {role.value}: No compiled agent, using baseline")
                specialized_agents[role.value] = agent

        except Exception as e:
            print(f"✗ Failed to load {role.value}: {e}")

    print(f"\nLoaded {len(specialized_agents)} nurse agents")
    print("=" * 70 + "\n")


class TriageRequest(BaseModel):
    """Request model for triage endpoint."""

    symptoms: str = Field(
        ...,
        description="Patient symptoms description",
        example="55-year-old with CHF, weight gain 5kg, increasing dyspnea, ankle swelling",
    )

    nurse_role: Optional[str] = Field(
        default="general_nurse",
        description="Specialized nurse role to use",
        example="chf_nurse",
    )


class TriageResponse(BaseModel):
    """Response model for triage endpoint."""

    triage_level: str = Field(description="Triage urgency level")
    clinical_justification: str = Field(description="Clinical reasoning")
    nurse_role: str = Field(description="Nurse specialization used")
    confidence_score: float = Field(
        default=0.95, description="Confidence in triage decision"
    )


@app.post("/triage", response_model=TriageResponse)
async def perform_triage(request: TriageRequest):
    """
    Triage endpoint with specialized nurse support.

    Evaluates patient symptoms using the specified nurse specialization.
    """
    # Validate nurse role
    try:
        role = NurseRole(request.nurse_role)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid nurse role: {request.nurse_role}. "
            f"Available: {[r.value for r in NurseRole]}",
        )

    # Get specialized agent
    if role.value not in specialized_agents:
        raise HTTPException(
            status_code=503,
            detail=f"Nurse agent '{role.value}' not loaded. Server starting up...",
        )

    agent = specialized_agents[role.value]

    try:
        result = agent.triage(request.symptoms)

        return TriageResponse(
            triage_level=result.triage_level,
            clinical_justification=result.clinical_justification,
            nurse_role=role.value,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage failed: {str(e)}")


@app.get("/nurses")
async def list_nurses():
    """List all available specialized nurse roles."""
    nurses = []

    for role_name, agent in specialized_agents.items():
        role = NurseRole(role_name)
        spec = get_specialization(role)

        # Check if agent is optimized
        compiled_path = Path(__file__).parent / f"compiled_{role.value}_agent.json"
        is_optimized = compiled_path.exists()

        nurses.append(
            {
                "role": role.value,
                "display_name": spec.display_name,
                "description": spec.description,
                "focus_symptoms": spec.focus_symptoms[:5],  # First 5
                "optimized": is_optimized,
                "status": "ready" if agent else "not_loaded",
            }
        )

    return {
        "total_nurses": len(nurses),
        "nurses": nurses,
    }


@app.get("/nurses/{role}")
async def get_nurse_details(role: str):
    """Get detailed information about a specific nurse role."""
    try:
        nurse_role = NurseRole(role)
    except ValueError:
        raise HTTPException(
            status_code=404, detail=f"Nurse role '{role}' not found"
        )

    spec = get_specialization(nurse_role)

    compiled_path = Path(__file__).parent / f"compiled_{role}_agent.json"

    return {
        "role": nurse_role.value,
        "display_name": spec.display_name,
        "description": spec.description,
        "focus_symptoms": spec.focus_symptoms,
        "focus_protocols": spec.focus_protocols,
        "min_training_cases": spec.min_training_cases,
        "optimized": compiled_path.exists(),
        "compiled_path": str(compiled_path) if compiled_path.exists() else None,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "total_agents": len(specialized_agents),
        "available_nurses": list(specialized_agents.keys()),
    }


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "STCC Specialized Nurse Triage API",
        "version": "2.0.0",
        "features": [
            "Multiple specialized nurse roles",
            "Domain-specific optimization",
            "Load/save compiled agents",
        ],
        "endpoints": {
            "triage": "/triage",
            "list_nurses": "/nurses",
            "nurse_details": "/nurses/{role}",
            "health": "/health",
            "docs": "/docs",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
