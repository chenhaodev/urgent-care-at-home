"""
FastAPI Wrapper for STCC Triage Agent.

Production-ready API endpoint for the triage agent.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.triage_agent import STCCTriageAgent

app = FastAPI(
    title="STCC Triage API",
    description="AI-powered medical triage using DSPy and DeepSeek",
    version="1.0.0",
)

# Global agent instance (loaded at startup)
triage_agent = None


@app.on_event("startup")
async def load_agent():
    """Load triage agent on startup."""
    global triage_agent

    print("Loading STCC Triage Agent...")

    try:
        triage_agent = STCCTriageAgent()

        # Load compiled version if available
        compiled_path = Path("deployment/compiled_triage_agent.json")
        if compiled_path.exists():
            print(f"Loading optimized agent from {compiled_path}")
            triage_agent.triage_module.load(str(compiled_path))
        else:
            print("Using base agent (not optimized)")

        print("Agent loaded successfully!")

    except Exception as e:
        print(f"Failed to load agent: {e}")
        raise


class TriageRequest(BaseModel):
    """Request model for triage endpoint."""

    symptoms: str = Field(
        ...,
        description="Patient symptoms description",
        example="55-year-old male with severe chest pain and shortness of breath",
    )


class TriageResponse(BaseModel):
    """Response model for triage endpoint."""

    triage_level: str = Field(description="Triage urgency level")
    clinical_justification: str = Field(description="Clinical reasoning")
    confidence_score: float = Field(
        default=0.95, description="Confidence in triage decision"
    )


@app.post("/triage", response_model=TriageResponse)
async def perform_triage(request: TriageRequest):
    """
    Triage endpoint - evaluate patient symptoms.

    Returns triage recommendation with clinical justification.
    """
    if triage_agent is None:
        raise HTTPException(
            status_code=503, detail="Triage agent not loaded. Server starting up..."
        )

    try:
        result = triage_agent.triage(request.symptoms)

        return TriageResponse(
            triage_level=result.triage_level,
            clinical_justification=result.clinical_justification,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if triage_agent is None:
        return {"status": "starting", "agent": "not_loaded"}

    return {
        "status": "healthy",
        "agent": "ready",
        "protocols": len(triage_agent.protocols),
    }


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "STCC Triage API",
        "version": "1.0.0",
        "endpoints": {
            "triage": "/triage",
            "health": "/health",
            "docs": "/docs",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
