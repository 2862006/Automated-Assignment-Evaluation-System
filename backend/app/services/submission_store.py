import uuid
from datetime import datetime
from typing import List, Tuple
from app.models.schemas import SubmissionRecord, GradeResponse, StatsResponse


_submissions: List[SubmissionRecord] = []
_answers: List[Tuple[str, str, str]] = []  # (student_name, subject, answer)


def save_submission(grade: GradeResponse, answer: str) -> SubmissionRecord:
    record = SubmissionRecord(
        id=str(uuid.uuid4())[:8],
        student_name=grade.student_name,
        subject=grade.subject,
        marks_obtained=grade.marks_obtained,
        max_marks=grade.max_marks,
        percentage=grade.percentage,
        grade_letter=grade.grade_letter,
        similarity_score=grade.plagiarism.similarity_percentage if grade.plagiarism else None,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    _submissions.append(record)
    _answers.append((grade.student_name, grade.subject, answer))
    return record


def get_previous_answers(subject: str, exclude_student: str) -> List[Tuple[str, str]]:
    """Get all previous answers for a subject (excluding current student)."""
    return [
        (name, ans)
        for name, subj, ans in _answers
        if subj == subject and name != exclude_student
    ]


def get_all_submissions() -> List[SubmissionRecord]:
    return list(reversed(_submissions))


def get_stats() -> StatsResponse:
    if not _submissions:
        return StatsResponse(
            total_submissions=0,
            average_score=0,
            highest_score=0,
            lowest_score=0,
            grade_distribution={},
        )

    scores = [s.percentage for s in _submissions]
    grade_dist = {}
    for s in _submissions:
        grade_dist[s.grade_letter] = grade_dist.get(s.grade_letter, 0) + 1

    return StatsResponse(
        total_submissions=len(_submissions),
        average_score=round(sum(scores) / len(scores), 1),
        highest_score=max(scores),
        lowest_score=min(scores),
        grade_distribution=grade_dist,
    )
