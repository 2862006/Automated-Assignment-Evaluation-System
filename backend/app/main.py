from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import grades, submissions, health

app = FastAPI(
    title="GradeAI API",
    description="Automate Grading & Feedback Using AI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(grades.router, prefix="/api/v1", tags=["Grades"])
app.include_router(submissions.router, prefix="/api/v1", tags=["Submissions"])

@app.get("/")
def root():
    return {"message": "GradeAI API is running 🚀", "docs": "/docs"}
