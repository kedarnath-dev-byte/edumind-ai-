"""
@module    tests.test_evaluation
@description Pytest tests for Feature 9 — Evaluation & Monitoring.
             Tests session tracking, document logging, question logging,
             RAGAS score generation, admin dashboard, and system health.
             Uses in-memory SQLite — no external services required.
@author    EduMind AI Engineering
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.database import Base
from backend.modules.evaluation.models import (
    StudentSession, DocumentHistory, QuestionHistory,
    RAGEvaluation, APIMetric,
)
from backend.modules.evaluation.evaluation_repository import EvaluationRepository
from backend.modules.evaluation.evaluation_service import EvaluationService


# ─── Test Database Setup ──────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh in-memory SQLite DB for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def service(db_session):
    """Return an EvaluationService wired to the test DB."""
    return EvaluationService(db_session)


@pytest.fixture(scope="function")
def repo(db_session):
    """Return an EvaluationRepository wired to the test DB."""
    return EvaluationRepository(db_session)


# ─── Test 1: Student Session Start ───────────────────────────────────────────

def test_start_student_session(service):
    """Session is created and returns session_id and email."""
    result = service.start_student_session(
        email="kedarnath@gmail.com",
        name="Kedarnath"
    )
    assert "session_id" in result
    assert result["student_email"] == "kedarnath@gmail.com"
    assert "started_at" in result


# ─── Test 2: Student Session End ─────────────────────────────────────────────

def test_end_student_session(service):
    """Session can be started and then ended cleanly."""
    start = service.start_student_session(email="test@gmail.com")
    session_id = start["session_id"]
    result = service.end_student_session(session_id=session_id)
    assert result["status"] == "session_ended"
    assert result["session_id"] == session_id


# ─── Test 3: Document Upload Logging ─────────────────────────────────────────

def test_log_document_upload(service):
    """Document upload is recorded with correct metadata."""
    result = service.log_document_upload(
        email="kedarnath@gmail.com",
        filename="ml_notes.pdf",
        file_type="pdf",
        file_size_kb=512.5,
        chunk_count=24,
        status="success",
    )
    assert result["filename"] == "ml_notes.pdf"
    assert result["status"] == "success"
    assert "doc_id" in result
    assert "uploaded_at" in result


# ─── Test 4: Student Document History ────────────────────────────────────────

def test_get_student_documents(service):
    """All documents for a student are returned correctly."""
    service.log_document_upload(
        email="student@gmail.com", filename="doc1.pdf",
        file_type="pdf", file_size_kb=100, chunk_count=10,
    )
    service.log_document_upload(
        email="student@gmail.com", filename="doc2.docx",
        file_type="docx", file_size_kb=200, chunk_count=15,
    )
    docs = service.get_student_documents(email="student@gmail.com")
    assert len(docs) == 2
    filenames = [d["filename"] for d in docs]
    assert "doc1.pdf" in filenames
    assert "doc2.docx" in filenames


# ─── Test 5: Question Logging + RAGAS Scores ─────────────────────────────────

def test_log_question_and_evaluate(service):
    """Question is logged and RAGAS scores are computed and stored."""
    result = service.log_question_and_evaluate(
        email="kedarnath@gmail.com",
        question="What is retrieval augmented generation?",
        answer="RAG combines retrieval with generation for better answers.",
        rag_type="naive",
        agent_used="tutor_agent",
        response_time_ms=340.5,
        context_chunks=5,
    )
    assert "question_id" in result
    assert "ragas_scores" in result
    scores = result["ragas_scores"]
    assert "faithfulness" in scores
    assert "answer_relevancy" in scores
    assert "context_precision" in scores
    assert "context_recall" in scores
    assert "overall_score" in scores
    # All scores should be between 0 and 1
    for key, val in scores.items():
        assert 0.0 <= val <= 1.0, f"{key} score out of range: {val}"


# ─── Test 6: Student Question History ────────────────────────────────────────

def test_get_student_questions(service):
    """All questions for a student are returned in history."""
    service.log_question_and_evaluate(
        email="student@gmail.com",
        question="What is LoRA?",
        answer="LoRA is a parameter-efficient fine-tuning method.",
        rag_type="hyde",
        agent_used="tutor_agent",
        response_time_ms=210.0,
        context_chunks=3,
    )
    service.log_question_and_evaluate(
        email="student@gmail.com",
        question="What is QLoRA?",
        answer="QLoRA adds quantization on top of LoRA.",
        rag_type="fusion",
        agent_used="tutor_agent",
        response_time_ms=195.0,
        context_chunks=4,
    )
    questions = service.get_student_questions(email="student@gmail.com")
    assert len(questions) == 2
    asked = [q["question"] for q in questions]
    assert "What is LoRA?" in asked
    assert "What is QLoRA?" in asked


# ─── Test 7: Admin Dashboard ──────────────────────────────────────────────────

def test_get_admin_dashboard(service):
    """Admin dashboard returns all required sections."""
    # Seed some data
    service.start_student_session(email="a@gmail.com", name="Student A")
    service.log_document_upload(
        email="a@gmail.com", filename="notes.pdf",
        file_type="pdf", file_size_kb=300, chunk_count=20,
    )
    service.log_question_and_evaluate(
        email="a@gmail.com",
        question="Explain transformers",
        answer="Transformers use self-attention mechanisms.",
        rag_type="rerank",
        agent_used="tutor_agent",
        response_time_ms=420.0,
        context_chunks=6,
    )
    dashboard = service.get_admin_dashboard()
    assert "system_health" in dashboard
    assert "avg_ragas_scores" in dashboard
    assert "recent_sessions" in dashboard
    assert "recent_documents" in dashboard
    assert "recent_questions" in dashboard
    assert dashboard["system_health"]["total_students"] >= 1
    assert dashboard["system_health"]["total_documents"] >= 1
    assert dashboard["system_health"]["total_questions"] >= 1


# ─── Test 8: API Metric Logging ───────────────────────────────────────────────

def test_log_api_metric(service):
    """API call metrics are logged correctly."""
    result = service.log_api_metric(
        endpoint="/api/v1/evaluation/question/log",
        method="POST",
        status_code=200,
        response_time_ms=145.3,
        student_email="kedarnath@gmail.com",
    )
    assert result["logged"] is True
    assert "metric_id" in result