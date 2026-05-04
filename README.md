# ◈ GradeAI — Automate Grading & Feedback Using AI

> AI-powered grading system that evaluates student answers, assigns marks, and generates detailed feedback — instantly.

![Tech Stack](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi)
![Tech Stack](https://img.shields.io/badge/React-Frontend-61DAFB?style=flat-square&logo=react)
![Tech Stack](https://img.shields.io/badge/Claude%20AI-Powered-6c63ff?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)

---

## Features

- **AI Grading** — Paste any question + student answer, get marks + feedback in seconds
- **Rubric Support** — Provide custom rubric for more accurate grading
- **Strengths & Improvements** — Detailed per-category feedback
- **Dashboard** — Grade distribution charts, stats, submission history
- **Bulk Grading** — Grade multiple submissions via API
- **Docker Ready** — One command to run everything

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI (Python 3.11) |
| AI Engine | Anthropic Claude (claude-sonnet) |
| Frontend | React 18 + Recharts |
| Container | Docker + Docker Compose |
| CI/CD | GitHub Actions → Docker Hub |

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/gradeai.git
cd gradeai
```

### 2. Set up environment

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run with Docker

```bash
docker-compose up --build
```

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/grade` | Grade a single submission |
| POST | `/api/v1/grade/bulk` | Grade multiple submissions |
| GET | `/api/v1/submissions` | Get all past submissions |
| GET | `/api/v1/stats` | Get grading statistics |
| GET | `/api/v1/health` | Health check |

### Example Request

```json
POST /api/v1/grade
{
  "student_name": "Rahul Sharma",
  "subject": "science",
  "question": "What is photosynthesis?",
  "answer": "Photosynthesis is the process by which plants make food using sunlight, water and CO2.",
  "max_marks": 10,
  "rubric": "3 marks definition, 4 marks process, 3 marks examples"
}
```

---

## GitHub Actions (CI/CD)

Add these secrets to your GitHub repo:
- `DOCKERHUB_USERNAME` — your Docker Hub username
- `DOCKERHUB_TOKEN` — Docker Hub access token

Every push to `main` automatically builds and pushes images to Docker Hub.

---

## Docker Hub

Pull and run directly:

```bash
docker pull YOUR_USERNAME/gradeai-backend:latest
docker pull YOUR_USERNAME/gradeai-frontend:latest
```

---

## Project Structure

```
gradeai/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── models/       # Pydantic schemas
│   │   ├── services/     # AI grader + store
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/   # GradeResult
│   │   ├── pages/        # GradePage, DashboardPage
│   │   └── utils/        # API client
│   ├── nginx.conf
│   └── Dockerfile
├── .github/workflows/    # CI/CD
├── docker-compose.yml
└── .env.example
```

---

## License

MIT
