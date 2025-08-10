from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.tmdb import search_people, get_person_details

router = APIRouter()


class PeopleSearchRequest(BaseModel):
    query: str
    page: int = 1


@router.post("/search")
def people_search(req: PeopleSearchRequest) -> Dict[str, Any]:
    return {"results": search_people(req.query, page=req.page)}


@router.get("/{person_id}")
def person_details(person_id: int) -> Dict[str, Any]:
    details = get_person_details(person_id)
    if not details:
        raise HTTPException(status_code=404, detail="Person not found")
    return details