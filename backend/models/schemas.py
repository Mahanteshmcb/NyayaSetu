from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class AnalyzeRequest(BaseModel):
    description: str = Field(..., min_length=5, max_length=8000, description="Describe the dispute in your own words")
    state: str = Field(default="Karnataka", min_length=2, max_length=100)
    language: Optional[str] = Field(default="auto", max_length=40)

    @field_validator("description")
    @classmethod
    def trim_description(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 5:
            raise ValueError("Please describe the situation in at least 5 characters.")
        return value

class SourceItem(BaseModel):
    source_id: str
    title: str
    authority: str
    jurisdiction: str
    score: Optional[float] = None
    provenance: str = "unknown"

class AnalyzeResponse(BaseModel):
    category: str
    confidence: float
    needs_clarification: bool
    clarification_question: Optional[str] = None
    explanation: str = ""
    sources: List[SourceItem] = []
    disclaimer: str = "Legal information only, not legal advice. Verify all sources with a qualified professional."
