<<<<<<< HEAD
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router

load_dotenv()
app = FastAPI(title="NyayaSetu API", version="0.1.0", description="Source-grounded legal-information prototype; not legal advice.")
origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
=======
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
>>>>>>> origin/main
