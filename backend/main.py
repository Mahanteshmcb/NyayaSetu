from fastapi import FastAPI, HTTPException

from backend.models.schemas import AnalyzeRequest, AnalyzeResponse
from backend.services.agent import analyze_case
from backend.services.validation import validate_description


app = FastAPI(
    title="NyayaSetu API",
    description=(
        "A source-grounded legal-information explainer "
        "for common disputes."
    ),
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "NyayaSetu",
    }


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    try:
        return analyze_case(
            description=request.description,
            state=request.state,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc