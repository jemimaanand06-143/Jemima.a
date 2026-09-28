from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie – Gemini-Powered Learning Assistant",
    version="1.0.0",
    description="A lightweight educational assistant with FastAPI and Google Gemini.",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30_000
    )


class QuizResponse(BaseModel):
    questions: list[dict[str, Any]]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie"
    }


@app.post("/qa")
async def qa(payload: TextRequest):
    try:
        return {
            "result": answer_question(payload.text)
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


@app.post("/explain")
async def explain(payload: TextRequest):
    try:
        return {
            "result": explain_concept(payload.text)
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


@app.post("/quiz", response_model=QuizResponse)
async def quiz(payload: TextRequest):
    try:
        return {
            "questions": generate_quiz(payload.text)
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        return {
            "result": summarize_text(payload.text)
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


@app.post("/learn/recommendations")
async def learn_recommendations(payload: TextRequest):
    try:
        return {
            "result": get_learning_recommendations(payload.text)
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc