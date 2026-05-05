"""
@module    evaluation.models
@description SQLAlchemy ORM models for student tracking, question history,
             document history, API metrics, and RAG evaluation scores.
             Follows Single Responsibility — pure data shape definitions only.
@author    EduMind AI Engineering
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from backend.core.database import Base


class StudentSession(Base):
    """Tracks every login session per student."""
    __tablename__ = "student_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String, index=True, nullable=False)
    student_name = Column(String, nullable=True)
    session_start = Column(DateTime, default=datetime.utcnow)
    session_end = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)


class DocumentHistory(Base):
    """Tracks every document uploaded by each student."""
    __tablename__ = "document_history"

    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String, index=True, nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size_kb = Column(Float, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    chunk_count = Column(Integer, default=0)
    status = Column(String, default="success")  # success | failed


class QuestionHistory(Base):
    """Tracks every question asked by each student and the RAG response."""
    __tablename__ = "question_history"

    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String, index=True, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    rag_type = Column(String, default="naive")
    agent_used = Column(String, nullable=True)
    asked_at = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Float, nullable=True)
    context_chunks_used = Column(Integer, default=0)


class RAGEvaluation(Base):
    """Stores RAGAS-style evaluation scores for each RAG response."""
    __tablename__ = "rag_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, index=True, nullable=False)
    faithfulness = Column(Float, nullable=True)   # 0.0 – 1.0
    answer_relevancy = Column(Float, nullable=True)
    context_precision = Column(Float, nullable=True)
    context_recall = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)
    evaluated_at = Column(DateTime, default=datetime.utcnow)


class APIMetric(Base):
    """Tracks API endpoint response times and status codes."""
    __tablename__ = "api_metrics"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Float, nullable=True)
    student_email = Column(String, nullable=True)
    called_at = Column(DateTime, default=datetime.utcnow)
    error_message = Column(Text, nullable=True)