from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from routers.quiz_router import router as quiz_router

app = FastAPI(title="Fist or Freeze API")

app.include_router(quiz_router)

@app.get('/')
def hello():
    return {
        "message": "Fist or Freeze API is running"
    }