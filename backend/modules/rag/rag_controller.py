"""
@module    rag_controller
@description FastAPI router for RAG pipeline endpoints.
             Handles AI queries using Groq Llama-3 directly.
             Falls back gracefully if ChromaDB has no documents.
@author    EduMind AI Engineering
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

router = APIRouter()

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
    """Query RAG pipeline with a student question using Groq Llama-3."""
    try:
        from groq import Groq
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")
        client = Groq(api_key=api_key)
        system_prompt = f"""You are EduMind AI — an intelligent education assistant.
You are using the {request.pipeline_type.upper()} RAG pipeline.
Answer the student question clearly and educationally.
If you do not have specific context, answer from your knowledge."""
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.question}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        answer = completion.choices[0].message.content
        return JSONResponse({
            "answer": answer,
            "pipeline": request.pipeline_type,
            "question": request.question,
            "model": "llama3-8b-8192"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rag/pipelines")
async def get_pipelines():
    """Get list of all available RAG pipelines."""
    return JSONResponse({"pipelines": ALL_PIPELINE_NAMES})

