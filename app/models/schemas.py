# ============================================================================
# Phases Schemas - Pydantic models for phase question extraction
# ============================================================================

from typing import List, Optional, Dict, Any, Literal, Union
from pydantic import BaseModel, Field
from app.config import settings


# =============================================================================
# REQUEST SCHEMAS
# =============================================================================

from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0




















class UserQuestion(BaseModel):
    """A question from the backend team's phases API."""
    phase_id: str = Field(..., description="Phase ID (e.g., 'phase_1')")
    question_id: str = Field(..., description="Question ID (e.g., 'q01_motivation')")
    text: str = Field(..., description="The question text")
    current_answer: Optional[str] = Field(None, description="Current answer if already answered")
    is_answered: bool = Field(False, description="Whether the question has been answered")
    answer_type: Optional[str] = Field(None, description="Expected answer type (string, number, boolean, etc.)")
    valid_values: Optional[List[str]] = Field(None, description="Valid values for the answer if applicable")
    extraction_hints: Optional[List[str]] = Field(None, description="Keywords to help extract answers")


class QuestionExtractionRequest(BaseModel):
    """Request to extract answers from user prompt."""
    user_id: str = Field(..., description="User ID (UUID format)")
    user_prompt: str = Field(..., description="The user's message to extract answers from")
    fetch_questions: bool = Field(True, description="If true, fetch questions from backend API. If false, use provided questions.")
    questions: Optional[List[Dict[str, Any]]] = Field(None, description="Optional: provide questions directly instead of fetching")


# =============================================================================
# RESPONSE SCHEMAS
# =============================================================================

class ExtractedAnswer(BaseModel):
    """An answer extracted from user's prompt."""
    question_id: str = Field(..., description="Question ID that was answered")
    question_text: Optional[str] = Field(None, description="The question text for display")
    phase_id: str = Field(..., description="Phase ID the question belongs to")
    raw_answer: Optional[str] = Field(None, description="User's exact words")
    answer: Any = Field(..., description="The normalized answer for storage")
    is_answered: Literal["true", "false", "modified", "not_applicable", "unclear"] = Field(
        ..., 
        description="'true' if new answer, 'modified' if changed, 'not_applicable' if doesn't apply, 'unclear' if needs clarification"
    )
    confidence: float = Field(0.8, description="Confidence score 0.0-1.0")
    needs_clarification: bool = Field(False, description="True if answer is ambiguous and needs follow-up")
    clarification_reason: Optional[str] = Field(None, description="Why clarification is needed")
    extraction_reason: Optional[str] = Field(None, description="Why this answer was extracted")


class QuestionExtractionResponse(BaseModel):
    """Response from question extraction."""
    success: bool
    user_id: str
    extracted_answers: List[ExtractedAnswer] = Field(default_factory=list)
    has_changes: bool = Field(False, description="True if any answers were extracted or modified")
    message: str = ""
    total_questions: int = Field(0, description="Total questions checked")
    questions_answered: int = Field(0, description="Questions with new/modified answers")


class PhasesQuestionsResponse(BaseModel):
    """Response from fetching user's phases and questions."""
    success: bool
    user_id: str
    phases: List[Dict[str, Any]] = Field(default_factory=list)
    total_questions: int = 0
    answered_count: int = 0
    unanswered_count: int = 0
    message: str = ""


# =============================================================================
# BACKEND API RESPONSE SCHEMA (what we expect from their API)
# =============================================================================

class BackendQuestionData(BaseModel):
    """Schema for question data from backend API."""
    id: str
    text: Optional[str] = None
    question: Optional[str] = None  # Some APIs use 'question' instead of 'text'
    phase_id: Optional[str] = None
    phaseId: Optional[str] = None  # Some APIs use camelCase
    is_answered: Optional[bool] = False
    isAnswered: Optional[bool] = False  # Some APIs use camelCase
    answer: Optional[str] = None
    current_answer: Optional[str] = None
    answer_type: Optional[str] = None
    valid_values: Optional[List[str]] = None

