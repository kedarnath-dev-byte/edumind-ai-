"""
@module    evaluation.evaluation_repository
@description Database access layer for all evaluation and monitoring data.
             Follows Repository Pattern — the ONLY layer allowed to run
             SQLAlchemy queries. Services call this; controllers call services.
@author    EduMind AI Engineering
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from backend.modules.evaluation.models import (
    StudentSession,
    DocumentHistory,
    QuestionHistory,
    RAGEvaluation,
    APIMetric,
)


class EvaluationRepository:
    """Handles all DB reads and writes for the evaluation module."""

    def __init__(self, db: Session):
        self.db = db

    # ─── Student Sessions ────────────────────────────────────────────────

    def create_session(self, email: str, name: Optional[str] = None) -> StudentSession:
        """Create a new student login session."""
        session = StudentSession(student_email=email, student_name=name)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def end_session(self, session_id: int) -> None:
        """Mark a session as ended."""
        session = self.db.query(StudentSession).filter(StudentSession.id == session_id).first()
        if session:
            session.session_end = datetime.utcnow()
            session.is_active = False
            self.db.commit()

    def get_all_sessions(self, limit: int = 100) -> List[StudentSession]:
        """Admin: get all student sessions, most recent first."""
        return self.db.query(StudentSession).order_by(desc(StudentSession.session_start)).limit(limit).all()

    # ─── Document History ────────────────────────────────────────────────

    def log_document(self, email: str, filename: str, file_type: str,
                     file_size_kb: float, chunk_count: int, status: str = "success") -> DocumentHistory:
        """Record a document upload event."""
        doc = DocumentHistory(
            student_email=email,
            filename=filename,
            file_type=file_type,
            file_size_kb=file_size_kb,
            chunk_count=chunk_count,
            status=status,
        )
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def get_documents_by_student(self, email: str) -> List[DocumentHistory]:
        """Get all documents uploaded by a specific student."""
        return self.db.query(DocumentHistory).filter(
            DocumentHistory.student_email == email
        ).order_by(desc(DocumentHistory.uploaded_at)).all()

    def get_all_documents(self, limit: int = 200) -> List[DocumentHistory]:
        """Admin: get all document uploads across all students."""
        return self.db.query(DocumentHistory).order_by(desc(DocumentHistory.uploaded_at)).limit(limit).all()

    # ─── Question History ────────────────────────────────────────────────

    def log_question(self, email: str, question: str, answer: str,
                     rag_type: str, agent_used: Optional[str],
                     response_time_ms: float, context_chunks: int) -> QuestionHistory:
        """Record a student question and its RAG answer."""
        q = QuestionHistory(
            student_email=email,
            question=question,
            answer=answer,
            rag_type=rag_type,
            agent_used=agent_used,
            response_time_ms=response_time_ms,
            context_chunks_used=context_chunks,
        )
        self.db.add(q)
        self.db.commit()
        self.db.refresh(q)
        return q

    def get_questions_by_student(self, email: str) -> List[QuestionHistory]:
        """Get all questions asked by a specific student."""
        return self.db.query(QuestionHistory).filter(
            QuestionHistory.student_email == email
        ).order_by(desc(QuestionHistory.asked_at)).all()

    def get_all_questions(self, limit: int = 500) -> List[QuestionHistory]:
        """Admin: get all questions across all students."""
        return self.db.query(QuestionHistory).order_by(desc(QuestionHistory.asked_at)).limit(limit).all()

    # ─── RAG Evaluation ──────────────────────────────────────────────────

    def log_rag_evaluation(self, question_id: int, faithfulness: float,
                           answer_relevancy: float, context_precision: float,
                           context_recall: float) -> RAGEvaluation:
        """Save RAGAS metric scores for a question."""
        overall = round(
            (faithfulness + answer_relevancy + context_precision + context_recall) / 4, 4
        )
        eval_record = RAGEvaluation(
            question_id=question_id,
            faithfulness=faithfulness,
            answer_relevancy=answer_relevancy,
            context_precision=context_precision,
            context_recall=context_recall,
            overall_score=overall,
        )
        self.db.add(eval_record)
        self.db.commit()
        self.db.refresh(eval_record)
        return eval_record

    def get_avg_rag_scores(self) -> dict:
        """Admin: get average RAGAS scores across all evaluations."""
        result = self.db.query(
            func.avg(RAGEvaluation.faithfulness).label("avg_faithfulness"),
            func.avg(RAGEvaluation.answer_relevancy).label("avg_relevancy"),
            func.avg(RAGEvaluation.context_precision).label("avg_precision"),
            func.avg(RAGEvaluation.context_recall).label("avg_recall"),
            func.avg(RAGEvaluation.overall_score).label("avg_overall"),
        ).first()
        return {
            "avg_faithfulness": round(result.avg_faithfulness or 0, 4),
            "avg_relevancy": round(result.avg_relevancy or 0, 4),
            "avg_precision": round(result.avg_precision or 0, 4),
            "avg_recall": round(result.avg_recall or 0, 4),
            "avg_overall": round(result.avg_overall or 0, 4),
        }

    # ─── API Metrics ─────────────────────────────────────────────────────

    def log_api_call(self, endpoint: str, method: str, status_code: int,
                     response_time_ms: float, student_email: Optional[str] = None,
                     error_message: Optional[str] = None) -> APIMetric:
        """Record one API call's performance data."""
        metric = APIMetric(
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time_ms=response_time_ms,
            student_email=student_email,
            error_message=error_message,
        )
        self.db.add(metric)
        self.db.commit()
        self.db.refresh(metric)
        return metric

    def get_avg_response_time(self) -> dict:
        """Admin: average response time per endpoint."""
        results = self.db.query(
            APIMetric.endpoint,
            func.avg(APIMetric.response_time_ms).label("avg_ms"),
            func.count(APIMetric.id).label("call_count"),
        ).group_by(APIMetric.endpoint).all()
        return [
            {"endpoint": r.endpoint, "avg_ms": round(r.avg_ms or 0, 2), "call_count": r.call_count}
            for r in results
        ]

    def get_system_health(self) -> dict:
        """Admin: high-level system health summary."""
        total_questions = self.db.query(func.count(QuestionHistory.id)).scalar()
        total_documents = self.db.query(func.count(DocumentHistory.id)).scalar()
        total_students = self.db.query(func.count(func.distinct(StudentSession.student_email))).scalar()
        active_sessions = self.db.query(func.count(StudentSession.id)).filter(
            StudentSession.is_active == True
        ).scalar()
        return {
            "total_students": total_students,
            "active_sessions": active_sessions,
            "total_documents": total_documents,
            "total_questions": total_questions,
        }