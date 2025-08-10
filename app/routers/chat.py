from typing import Optional, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.tmdb import search_movies, search_people, discover_movies_by_language, search_people_tamil
from app.services.image_gen import generate_image
from app.memory.in_memory import ChatMemory
from app.data.tamil_people import TAMIL_PEOPLE_CURATED

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
    lower = req.message.lower()

    tamil_focus = any(k in lower for k in ["kollywood", "tamil"])

    movies_intent = any(k in lower for k in ["movie", "film", "bollywood", "tollywood", "kollywood"]) or "movies" in lower
    people_intent = any(k in lower for k in ["actor", "actress", "star", "celebrity", "person"]) or "actors" in lower or "actresses" in lower

    if movies_intent:
        if tamil_focus:
            info["movies"] = discover_movies_by_language(lang="ta")
        else:
            info["movies"] = search_movies(req.message)

    if people_intent:
        if tamil_focus:
            filtered = search_people_tamil(req.message)
            if not filtered:
                info["people_curated"] = TAMIL_PEOPLE_CURATED
            info["people"] = filtered
        else:
            info["people"] = search_people(req.message)

    # If the user asked broadly about tamil/kollywood but intents not captured, still provide curated people
    if tamil_focus and not info.get("people") and not info.get("people_curated"):
        info["people_curated"] = TAMIL_PEOPLE_CURATED

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