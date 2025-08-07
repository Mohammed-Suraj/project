## Bollywood Chatbot API

A FastAPI service that:
- Aggregates information about Indian movies and celebrities via TMDB
- Generates images from text prompts using OpenAI, Stability, or a dummy placeholder provider
- Maintains simple in-memory chat session history

### Setup
1. Create and populate `.env` (see `.env.example`). At minimum, set:
   - `TMDB_API_KEY` from themoviedb.org (free)
   - `IMAGE_PROVIDER` = `openai` | `stability` | `dummy`
   - Corresponding API key(s) if not using `dummy`

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Endpoints
- `GET /health` – health check
- `POST /chat` – chat orchestration
  - Body: `{ "session_id": "abc", "message": "Who is Shah Rukh Khan?", "generate_image": true }`
- `POST /movies/search` – movie search
- `GET /movies/{movie_id}` – movie details
- `POST /people/search` – people search
- `GET /people/{person_id}` – person details
- `POST /generate-image` – coming from chat; use `IMAGE_PROVIDER`

### Notes
- If you do not set image API keys, `IMAGE_PROVIDER=dummy` returns a placeholder image, allowing you to test end-to-end.
- The chat intent detection is rule-based for reliability without an LLM. You can replace it with an LLM later for richer UX.