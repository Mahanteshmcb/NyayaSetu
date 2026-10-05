from fastapi import FastAPI

from backend.models.schemas import AnalyzeRequest, AnalyzeResponse
from backend.services.agent import analyze_case


app = FastAPI(
    title="NyayaSetu API",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "NyayaSetu"
    }


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):

    return analyze_case(
        description=request.description,
        state=request.state
    )