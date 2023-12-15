from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from api.end_points.search_to_provider import generate_gpt_response

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class InputMessage(BaseModel):
    input_mes: str
    in_provider: str


class OutputResult(BaseModel):
    response: list


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate-keywords", response_model=OutputResult)
def generate_keywords(input_api: InputMessage):
    try:
        result = generate_gpt_response(input_api.in_provider, input_api.input_mes)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=6080)
