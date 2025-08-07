from typing import Any, Dict, List, Optional
import requests

from app.config import TMDB_API_KEY

TMDB_BASE_URL = "https://api.themoviedb.org/3"


def _tmdb_get(path: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    if TMDB_API_KEY is None:
        return None
    url = f"{TMDB_BASE_URL}{path}"
    params = params or {}
    params["api_key"] = TMDB_API_KEY
    params.setdefault("language", "en-US")
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def search_movies(query: str, page: int = 1) -> List[Dict[str, Any]]:
    data = _tmdb_get("/search/movie", {"query": query, "page": page})
    if not data:
        return []
    return data.get("results", [])


def get_movie_details(movie_id: int) -> Optional[Dict[str, Any]]:
    data = _tmdb_get(f"/movie/{movie_id}", {"append_to_response": "credits,images,release_dates"})
    return data


def search_people(query: str, page: int = 1) -> List[Dict[str, Any]]:
    data = _tmdb_get("/search/person", {"query": query, "page": page})
    if not data:
        return []
    return data.get("results", [])


def get_person_details(person_id: int) -> Optional[Dict[str, Any]]:
    data = _tmdb_get(f"/person/{person_id}", {"append_to_response": "combined_credits,images"})
    return data