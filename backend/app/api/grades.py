from fastapi import APIRouter, HTTPException
from app.models.schemas import GradeRequest, GradeResponse, BulkGradeRequest, PlagiarismCheckRequest
from app.services.ai_grader import grade_submission
from app.services.plagiarism import check_similarity, check_against_all
from app.services.submission_store import save_submission, get_previous_answers

router = APIRouter()


@router.post("/grade", response_model=GradeResponse)
async def grade_answer(request: GradeRequest):
    """Grade a single student submission using AI with plagiarism check."""
    try:
        # Check plagiarism against previous submissions of same subject
        prev_answers = get_previous_answers(request.subject.value, request.student_name)
        plagiarism_result = check_against_all(request.answer, prev_answers)

        result = await grade_submission(request, plagiarism_result)
        save_submission(result, request.answer)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Grading failed: {str(e)}")


@router.post("/grade/bulk")
async def grade_bulk(request: BulkGradeRequest):
    """Grade multiple submissions with cross-plagiarism detection."""
    results = []
    errors = []
    graded_answers = []  # track answers graded so far for cross-check

    for i, submission in enumerate(request.submissions):
        try:
            # Check against already graded submissions in this batch + stored ones
            prev_from_store = get_previous_answers(submission.subject.value, submission.student_name)
            prev_combined = prev_from_store + graded_answers

            plagiarism_result = check_against_all(submission.answer, prev_combined) if request.check_plagiarism else None

            result = await grade_submission(submission, plagiarism_result)
            save_submission(result, submission.answer)
            results.append(result)
            graded_answers.append((submission.student_name, submission.answer))
        except Exception as e:
            errors.append({"index": i, "student": submission.student_name, "error": str(e)})

    return {"graded": results, "errors": errors, "total": len(request.submissions)}


@router.post("/plagiarism/check")
def check_plagiarism(request: PlagiarismCheckRequest):
    """Directly compare two texts for similarity."""
    result = check_similarity(request.text1, request.text2, request.student2)
    return {
        "student1": request.student1,
        "student2": request.student2,
        "result": result,
    }

