from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.tmdb import search_movies, get_movie_details

router = APIRouter()


class MovieSearchRequest(BaseModel):
    query: str
    page: int = 1


@router.post("/search")
def movies_search(req: MovieSearchRequest) -> Dict[str, Any]:
    return {"results": search_movies(req.query, page=req.page)}


@router.get("/{movie_id}")
def movie_details(movie_id: int) -> Dict[str, Any]:
    details = get_movie_details(movie_id)
    if not details:
        raise HTTPException(status_code=404, detail="Movie not found")
    return details