from typing import Optional, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.tmdb import search_movies, search_people
from app.services.image_gen import generate_image
from app.memory.in_memory import ChatMemory

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    message: str
    image_prompt: Optional[str] = None
    generate_image: bool = False
    image_size: Optional[str] = None  # e.g., "1024x1024"


@router.post("")
def chat(req: ChatRequest) -> Dict[str, Any]:
    ChatMemory.add_message(req.session_id, role="user", content=req.message)

    info: Dict[str, Any] = {}
    # Very lightweight intent heuristics
    lower = req.message.lower()
    if any(k in lower for k in ["movie", "film", "bollywood", "tollywood", "kollywood"]):
        info["movies"] = search_movies(req.message)
    if any(k in lower for k in ["actor", "actress", "star", "celebrity", "person"]):
        info["people"] = search_people(req.message)

    image = None
    if req.generate_image or req.image_prompt:
        prompt = req.image_prompt or req.message
        image = generate_image(prompt=prompt, size=req.image_size)

    assistant_message = {
        "info": info,
        "image": image,
    }
    ChatMemory.add_message(req.session_id, role="assistant", content=assistant_message)

    history = ChatMemory.get_history(req.session_id)
    return {
        "message": assistant_message,
        "history": history,
    }