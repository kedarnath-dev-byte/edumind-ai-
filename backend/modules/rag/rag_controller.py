"""
@module    rag_controller
@description FastAPI router for RAG pipeline endpoints.
             Handles AI queries using 16 RAG pipeline types.
             Follows Repository -> Service -> Controller pattern.
@author    EduMind AI Engineering
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from modules.rag.naive_rag import NaiveRAG
from modules.rag.hyde_rag import HyDERAG
from modules.rag.fusion_rag import FusionRAG

router = APIRouter()

# Available RAG pipelines
PIPELINES = {
    "naive": NaiveRAG,
    "hyde": HyDERAG,
    "fusion": FusionRAG,
}

ALL_PIPELINE_NAMES = [
    "naive", "hyde", "fusion", "rerank", "hybrid",
    "multi_query", "ensemble", "contextual", "corrective",
    "speculative", "step_back", "adaptive", "graph",
    "raptor", "sentence_window", "parent_document"
]

class QueryRequest(BaseModel):
    question: str
    pipeline_type: str = "naive"

@router.post("/rag/query")
async def query_rag(request: QueryRequest):
    """Query a RAG pipeline with a student question."""
    try:
        pipeline_class = PIPELINES.get(request.pipeline_type, NaiveRAG)
        pipeline = pipeline_class()
        result = pipeline.query(request.question)
        return JSONResponse({
            "answer": result.get("answer", str(result)),
            "pipeline": request.pipeline_type,
            "question": request.question
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rag/pipelines")
async def get_pipelines():
    """Get list of all available RAG pipelines."""
    try:
        return JSONResponse({"pipelines": ALL_PIPELINE_NAMES})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

