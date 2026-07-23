import uuid
import logging
import asyncio
from core.llm_client import LLMClient
from models.quiz import QuestionModel, AnswerResponse

logger = logging.getLogger(__name__)
SESSIONS = {}
BUFFER_SIZE=2

class QuizService:
    def __init__(self):
        self.llm_client = LLMClient()
    
    async def _fil_buffer(self, session_id: str):
        session = SESSIONS.get(session_id)
        if not session:
            return
        
        queue: asyncio.Queue = session["question_queue"]
        
        while queue.qsize() < BUFFER_SIZE and session["is_active"]:
            try:
                logger.info(f"[Sesion {session_id}] Pre-buffering question...")
                question = await self.llm_client.generate_question(
                    category=session["category"],
                    difficulty=session["difficulty"]
                )
                await queue.put(question)
                logger.info(f"[Session {session_id}] Question added to buffer. Queue size: {queue.qsize()}")
            except Exception as e:
                logger.error(f"[Session {session_id}] Error generating background question: {e}")
                await asyncio.sleep(1)
    
    async def start_new_game(self, category: str, difficulty: str):
        session_id = str(uuid.uuid4())
        SESSIONS[session_id] = {
            "category": category,
            "difficulty": difficulty,
            "score": 0,
            "current_question": None,
            "question_queue": asyncio.Queue(),
            "is_active": True
        }
        
        asyncio.create_task(self._fil_buffer(session_id))
        return session_id
    
    async def get_next_question(self, session_id: str) -> QuestionModel:
        session = SESSIONS.get(session_id)
        if not session:
            raise ValueError("Session not found")
        
        queue: asyncio.Queue = session["question_queue"]
        question = await queue.get()
        # TODO: ใช้ Ollama
        # question = await self.llm_client.generate_question(
        #     category=session["category"],
        #     difficulty=session["difficulty"]
        # )
        
        session["current_question"] = question
        asyncio.create_task(self._fil_buffer(session_id))
        return question
    
    def check_answer(self, session_id: str, selected_option: str) -> AnswerResponse:
        session = SESSIONS.get(session_id)
        if not session or not session["current_question"]:
            raise ValueError("Invalid session or no active question")
        
        current_q = session["current_question"]
        is_correct = (selected_option.strip().upper() == current_q.correct_option.strip().upper())
        
        if is_correct:
            session["score"] += 1
        
        return AnswerResponse(
            is_correct= is_correct,
            correct_option= current_q.correct_option,
            explanation= current_q.explanation,
            current_score= session["score"]
        )
        
    def end_game(self, session_id: str) -> dict:
        session = SESSIONS.get(session_id)
        if not session:
            raise ValueError("Session not found")
        
        session["is_active"] = False
        final_score = session["score"]
        
        del SESSIONS[session_id]
        
        return {
            "final_score": final_score,
            "message": "Game is ended"
        }