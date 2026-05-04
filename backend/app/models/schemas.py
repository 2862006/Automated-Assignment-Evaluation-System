from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class SubjectType(str, Enum):
    MATH = "math"
    SCIENCE = "science"
    ENGLISH = "english"
    HISTORY = "history"
    CODING = "coding"
    OTHER = "other"


class GradeRequest(BaseModel):
    student_name: str
    subject: SubjectType
    question: str
    answer: str
    max_marks: int = 10
    rubric: Optional[str] = None
    is_coding: bool = False  # True = evaluate as code


class FeedbackItem(BaseModel):
    category: str
    comment: str
    suggestion: str


class PlagiarismResult(BaseModel):
    similarity_score: float        # 0.0 to 1.0
    similarity_percentage: float   # 0 to 100
    risk_level: str                # Low / Medium / High
    matched_with: Optional[str]    # student name if matched
    verdict: str                   # Original / Suspicious / Plagiarised


class GradeResponse(BaseModel):
    student_name: str
    subject: str
    marks_obtained: float
    max_marks: int
    percentage: float
    grade_letter: str
    overall_feedback: str
    strengths: List[str]
    improvements: List[str]
    detailed_feedback: List[FeedbackItem]
    plagiarism: Optional[PlagiarismResult] = None


class SubmissionRecord(BaseModel):
    id: str
    student_name: str
    subject: str
    marks_obtained: float
    max_marks: int
    percentage: float
    grade_letter: str
    similarity_score: Optional[float] = None
    timestamp: str


class BulkGradeRequest(BaseModel):
    submissions: List[GradeRequest]
    check_plagiarism: bool = True   # Compare submissions against each other


class PlagiarismCheckRequest(BaseModel):
    text1: str
    text2: str
    student1: str
    student2: str


class StatsResponse(BaseModel):
    total_submissions: int
    average_score: float
    highest_score: float
    lowest_score: float
    grade_distribution: dict
