"""
@module    evaluation.evaluation_service
@description Business logic layer for evaluation and monitoring.
             Computes RAGAS-style scores, aggregates admin dashboard data,
             and formats system health reports.
             Delegates all DB access to EvaluationRepository.
@author    EduMind AI Engineering
"""

import random
from typing import Optional
from sqlalchemy.orm import Session

from modules.evaluation.evaluation_repository import EvaluationRepository


class EvaluationService:
    """Orchestrates evaluation logic — no direct DB access allowed here."""

    def __init__(self, db: Session):
        self.repo = EvaluationRepository(db)

    # ─── Student Tracking ────────────────────────────────────────────────

    def start_student_session(self, email: str, name: Optional[str] = None) -> dict:
        """Begin tracking a student login session."""
        try:
            session = self.repo.create_session(email=email, name=name)
            return {
                "session_id": session.id,
                "student_email": session.student_email,
                "started_at": session.session_start.isoformat(),
            }
        except Exception as e:
            return {"error": str(e)}

    def end_student_session(self, session_id: int) -> dict:
        """End a student session on logout."""
        try:
            self.repo.end_session(session_id)
            return {"status": "session_ended", "session_id": session_id}
        except Exception as e:
            return {"error": str(e)}

    # ─── Document Logging ────────────────────────────────────────────────

    def log_document_upload(self, email: str, filename: str, file_type: str,
                            file_size_kb: float, chunk_count: int,
                            status: str = "success") -> dict:
        """Record a document upload event for a student."""
        try:
            doc = self.repo.log_document(
                email=email,
                filename=filename,
                file_type=file_type,
                file_size_kb=file_size_kb,
                chunk_count=chunk_count,
                status=status,
            )
            return {
                "doc_id": doc.id,
                "filename": doc.filename,
                "status": doc.status,
                "uploaded_at": doc.uploaded_at.isoformat(),
            }
        except Exception as e:
            return {"error": str(e)}

    def get_student_documents(self, email: str) -> list:
        """Return all documents uploaded by a student."""
        try:
            docs = self.repo.get_documents_by_student(email)
            return [
                {
                    "id": d.id,
                    "filename": d.filename,
                    "file_type": d.file_type,
                    "file_size_kb": d.file_size_kb,
                    "chunk_count": d.chunk_count,
                    "status": d.status,
                    "uploaded_at": d.uploaded_at.isoformat(),
                }
                for d in docs
            ]
        except Exception as e:
            return [{"error": str(e)}]

    # ─── Question Logging ────────────────────────────────────────────────

    def log_question_and_evaluate(self, email: str, question: str, answer: str,
                                  rag_type: str, agent_used: Optional[str],
                                  response_time_ms: float, context_chunks: int) -> dict:
        """
        Log a student question and auto-compute simulated RAGAS scores.
        In production, replace simulate_ragas_scores() with real RAGAS calls.
        """
        try:
            q = self.repo.log_question(
                email=email,
                question=question,
                answer=answer,
                rag_type=rag_type,
                agent_used=agent_used,
                response_time_ms=response_time_ms,
                context_chunks=context_chunks,
            )
            # Compute RAGAS scores
            scores = self._simulate_ragas_scores(question, answer, context_chunks)
            eval_record = self.repo.log_rag_evaluation(
                question_id=q.id,
                faithfulness=scores["faithfulness"],
                answer_relevancy=scores["answer_relevancy"],
                context_precision=scores["context_precision"],
                context_recall=scores["context_recall"],
            )
            return {
                "question_id": q.id,
                "response_time_ms": response_time_ms,
                "ragas_scores": {
                    "faithfulness": eval_record.faithfulness,
                    "answer_relevancy": eval_record.answer_relevancy,
                    "context_precision": eval_record.context_precision,
                    "context_recall": eval_record.context_recall,
                    "overall_score": eval_record.overall_score,
                },
            }
        except Exception as e:
            return {"error": str(e)}

    def _simulate_ragas_scores(self, question: str, answer: str, context_chunks: int) -> dict:
        """
        Simulate RAGAS metric scores based on heuristics.
        Replace with real ragas library calls when GPU/API budget allows.
        Scores are 0.0 – 1.0; higher is better.
        """
        base = min(0.95, 0.60 + (context_chunks * 0.05))
        return {
            "faithfulness":       round(min(1.0, base + random.uniform(-0.05, 0.05)), 4),
            "answer_relevancy":   round(min(1.0, base + random.uniform(-0.05, 0.05)), 4),
            "context_precision":  round(min(1.0, base + random.uniform(-0.08, 0.08)), 4),
            "context_recall":     round(min(1.0, base + random.uniform(-0.08, 0.08)), 4),
        }

    def get_student_questions(self, email: str) -> list:
        """Return full question history for one student."""
        try:
            questions = self.repo.get_questions_by_student(email)
            return [
                {
                    "id": q.id,
                    "question": q.question,
                    "answer": q.answer,
                    "rag_type": q.rag_type,
                    "agent_used": q.agent_used,
                    "response_time_ms": q.response_time_ms,
                    "context_chunks_used": q.context_chunks_used,
                    "asked_at": q.asked_at.isoformat(),
                }
                for q in questions
            ]
        except Exception as e:
            return [{"error": str(e)}]

    # ─── Admin Dashboard ─────────────────────────────────────────────────

    def get_admin_dashboard(self) -> dict:
        """Return complete admin view: health + all students + RAG scores + API metrics."""
        try:
            health = self.repo.get_system_health()
            all_sessions = self.repo.get_all_sessions(limit=50)
            all_documents = self.repo.get_all_documents(limit=100)
            all_questions = self.repo.get_all_questions(limit=200)
            avg_ragas = self.repo.get_avg_rag_scores()
            api_metrics = self.repo.get_avg_response_time()

            return {
                "system_health": health,
                "avg_ragas_scores": avg_ragas,
                "api_performance": api_metrics,
                "recent_sessions": [
                    {
                        "id": s.id,
                        "student_email": s.student_email,
                        "student_name": s.student_name,
                        "session_start": s.session_start.isoformat(),
                        "is_active": s.is_active,
                    }
                    for s in all_sessions
                ],
                "recent_documents": [
                    {
                        "id": d.id,
                        "student_email": d.student_email,
                        "filename": d.filename,
                        "status": d.status,
                        "uploaded_at": d.uploaded_at.isoformat(),
                    }
                    for d in all_documents
                ],
                "recent_questions": [
                    {
                        "id": q.id,
                        "student_email": q.student_email,
                        "question": q.question[:80] + "..." if len(q.question) > 80 else q.question,
                        "rag_type": q.rag_type,
                        "response_time_ms": q.response_time_ms,
                        "asked_at": q.asked_at.isoformat(),
                    }
                    for q in all_questions
                ],
            }
        except Exception as e:
            return {"error": str(e)}

    # ─── API Metrics ─────────────────────────────────────────────────────

    def log_api_metric(self, endpoint: str, method: str, status_code: int,
                       response_time_ms: float, student_email: Optional[str] = None,
                       error_message: Optional[str] = None) -> dict:
        """Log one API call's performance."""
        try:
            metric = self.repo.log_api_call(
                endpoint=endpoint,
                method=method,
                status_code=status_code,
                response_time_ms=response_time_ms,
                student_email=student_email,
                error_message=error_message,
            )
            return {"metric_id": metric.id, "logged": True}
        except Exception as e:
            return {"error": str(e)}

