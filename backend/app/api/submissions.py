from fastapi import APIRouter
from app.services.submission_store import get_all_submissions, get_stats

router = APIRouter()


@router.get("/submissions")
def list_submissions():
    """Get all past submissions."""
    return get_all_submissions()


@router.get("/stats")
def get_statistics():
    """Get grading statistics."""
    return get_stats()
