import os
import json
import re
import anthropic
from app.models.schemas import GradeRequest, GradeResponse, FeedbackItem, PlagiarismResult
from typing import Optional

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))


def calculate_grade_letter(percentage: float) -> str:
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def _build_descriptive_prompt(request: GradeRequest) -> str:
    rubric_text = f"\nRubric: {request.rubric}" if request.rubric else ""
    return f"""You are an expert teacher grading a student's descriptive answer. Grade strictly and fairly.

Subject: {request.subject.value.upper()}
Question: {request.question}
Student's Answer: {request.answer}
Maximum Marks: {request.max_marks}{rubric_text}

Evaluate and respond ONLY with valid JSON (no markdown, no extra text):
{{
  "marks_obtained": <number between 0 and {request.max_marks}>,
  "overall_feedback": "<2-3 sentence summary>",
  "strengths": ["<strength 1>", "<strength 2>"],
  "improvements": ["<area 1>", "<area 2>"],
  "detailed_feedback": [
    {{"category": "Content Accuracy", "comment": "<comment>", "suggestion": "<suggestion>"}},
    {{"category": "Clarity & Structure", "comment": "<comment>", "suggestion": "<suggestion>"}}
  ]
}}"""


def _build_coding_prompt(request: GradeRequest) -> str:
    rubric_text = f"\nRubric: {request.rubric}" if request.rubric else ""
    return f"""You are an expert programming instructor grading a student's code submission.

Problem Statement: {request.question}
Student's Code:
```
{request.answer}
```
Maximum Marks: {request.max_marks}{rubric_text}

Evaluate the code on: correctness, logic, edge cases, code quality, efficiency, and best practices.
Respond ONLY with valid JSON (no markdown, no extra text):
{{
  "marks_obtained": <number between 0 and {request.max_marks}>,
  "overall_feedback": "<2-3 sentence summary of the code quality>",
  "strengths": ["<strength 1>", "<strength 2>"],
  "improvements": ["<improvement 1>", "<improvement 2>"],
  "detailed_feedback": [
    {{"category": "Correctness & Logic", "comment": "<comment>", "suggestion": "<suggestion>"}},
    {{"category": "Code Quality & Style", "comment": "<comment>", "suggestion": "<suggestion>"}},
    {{"category": "Efficiency & Edge Cases", "comment": "<comment>", "suggestion": "<suggestion>"}}
  ]
}}"""


async def grade_submission(
    request: GradeRequest,
    plagiarism_result: Optional[PlagiarismResult] = None
) -> GradeResponse:

    # Choose prompt based on submission type
    if request.is_coding or request.subject.value == "coding":
        prompt = _build_coding_prompt(request)
    else:
        prompt = _build_descriptive_prompt(request)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = message.content[0].text.strip()
    response_text = re.sub(r"^```(?:json)?\s*", "", response_text)
    response_text = re.sub(r"\s*```$", "", response_text)

    data = json.loads(response_text)

    marks = float(data["marks_obtained"])
    percentage = round((marks / request.max_marks) * 100, 1)

    return GradeResponse(
        student_name=request.student_name,
        subject=request.subject.value,
        marks_obtained=marks,
        max_marks=request.max_marks,
        percentage=percentage,
        grade_letter=calculate_grade_letter(percentage),
        overall_feedback=data["overall_feedback"],
        strengths=data.get("strengths", []),
        improvements=data.get("improvements", []),
        detailed_feedback=[
            FeedbackItem(**fb) for fb in data.get("detailed_feedback", [])
        ],
        plagiarism=plagiarism_result,
    )
