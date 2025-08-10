import os
from typing import Optional
from dotenv import load_dotenv

# Load variables from .env if present
load_dotenv()


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value


TMDB_API_KEY = get_env("TMDB_API_KEY")
IMAGE_PROVIDER = (get_env("IMAGE_PROVIDER", "dummy") or "dummy").lower()
OPENAI_API_KEY = get_env("OPENAI_API_KEY")
STABILITY_API_KEY = get_env("STABILITY_API_KEY")
DEFAULT_IMAGE_SIZE = get_env("DEFAULT_IMAGE_SIZE", "1024x1024")