from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from api.end_points.search_to_provider import generate_gpt_response
from api.end_points.google_generative import GoogleGenerative

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class InputMessageKW(BaseModel):
    input_mes: str
    in_provider: str


class OutputResultKW(BaseModel):
    response: str


class InputMessageGO(BaseModel):
    input_mes: str


class OutputResultGo(BaseModel):
    response: str


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate-keywords", response_model=OutputResultKW)
def generate_keywords(input_api: InputMessageKW):
    try:
        result = generate_gpt_response(input_api.in_provider, input_api.input_mes)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/google_generative", response_model=OutputResultGo)
def generative_google(input_mes: InputMessageGO):
    google_ge = GoogleGenerative()
    try:
        result = google_ge.generative(input_mes=input_mes.input_mes)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=6080)
