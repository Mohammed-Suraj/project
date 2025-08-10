from typing import Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.image_gen import generate_image

router = APIRouter()


class ImageGenRequest(BaseModel):
    prompt: str
    size: Optional[str] = None


@router.post("")
def image_generate(req: ImageGenRequest) -> Dict[str, Any]:
    return generate_image(prompt=req.prompt, size=req.size)