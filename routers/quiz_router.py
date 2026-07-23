from fastapi import APIRouter, HTTPException
from models.quiz import StartGameRequest, SubmitAnswerRequest
from services.quiz_service import QuizService

router = APIRouter(prefix="/api/v1/quiz", tags=["Quiz"])
quiz_service = QuizService()

@router.post("/start")
async def start_game(payload: StartGameRequest):
    try:
        session_id = await quiz_service.start_new_game(payload.category, payload.difficulty)
        return {
            "session_id": session_id, 
            "message": "Game started"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/question/{session_id}")
async def get_question(session_id: str):
    try:
        question = await quiz_service.get_next_question(session_id)
        return {
            "question": question.question,
            "options": question.options
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/answer")
async def submi_answer(payload: SubmitAnswerRequest):
    try:
        result = quiz_service.check_answer(payload.session_id, payload.selected_option)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/endgame/{session_id}")
async def end_game(session_id: str):
    try:
        result = quiz_service.end_game(session_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))