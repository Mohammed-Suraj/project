import base64
from typing import Any, Dict, Optional
import requests

from app.config import IMAGE_PROVIDER, OPENAI_API_KEY, STABILITY_API_KEY, DEFAULT_IMAGE_SIZE


def _generate_with_openai(prompt: str, size: Optional[str]) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        return _generate_with_dummy(prompt, size)
    try:
        # OpenAI Images API (gpt-image-1)
        url = "https://api.openai.com/v1/images/generations"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "gpt-image-1", "prompt": prompt, "size": size or DEFAULT_IMAGE_SIZE}
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        image_b64 = data.get("data", [{}])[0].get("b64_json")
        return {"provider": "openai", "image_base64": image_b64, "image_url": None}
    except Exception as e:
        return {"provider": "openai", "error": str(e)}


def _generate_with_stability(prompt: str, size: Optional[str]) -> Dict[str, Any]:
    if not STABILITY_API_KEY:
        return _generate_with_dummy(prompt, size)
    try:
        # Stability REST (Stable Diffusion XL)
        # Note: Size may be ignored; defaulting to 1024x1024-like outputs depending on the engine
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        headers = {"Authorization": f"Bearer {STABILITY_API_KEY}"}
        form = {"text_prompts[0][text]": prompt, "cfg_scale": 7, "steps": 30}
        resp = requests.post(url, headers=headers, files={}, data=form, timeout=60)
        if resp.status_code == 200:
            json_data = resp.json()
            artifacts = json_data.get("artifacts", [])
            if artifacts:
                b64 = artifacts[0].get("base64")
                return {"provider": "stability", "image_base64": b64, "image_url": None}
        return {"provider": "stability", "error": f"HTTP {resp.status_code}: {resp.text[:200]}"}
    except Exception as e:
        return {"provider": "stability", "error": str(e)}


def _generate_with_dummy(prompt: str, size: Optional[str]) -> Dict[str, Any]:
    # Return a placeholder image fetched and re-encoded as base64
    try:
        text = requests.utils.quote(prompt[:50] or "Image")
        size_str = size or DEFAULT_IMAGE_SIZE
        w, h = size_str.split("x") if "x" in size_str else ("1024", "1024")
        url = f"https://placehold.co/{w}x{h}?text={text}"
        img = requests.get(url, timeout=30)
        img.raise_for_status()
        b64 = base64.b64encode(img.content).decode("utf-8")
        return {"provider": "dummy", "image_base64": b64, "image_url": url}
    except Exception as e:
        return {"provider": "dummy", "error": str(e)}


def generate_image(prompt: str, size: Optional[str] = None) -> Dict[str, Any]:
    provider = IMAGE_PROVIDER
    if provider == "openai":
        return _generate_with_openai(prompt, size)
    if provider == "stability":
        return _generate_with_stability(prompt, size)
    return _generate_with_dummy(prompt, size)