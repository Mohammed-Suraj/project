from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import os

from app.routers.chat import router as chat_router
from app.routers.movies import router as movies_router
from app.routers.people import router as people_router
from app.routers.image import router as image_router

app = FastAPI(title="Bollywood Chatbot API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(chat_router, prefix="/chat", tags=["chat"]) 
app.include_router(movies_router, prefix="/movies", tags=["movies"]) 
app.include_router(people_router, prefix="/people", tags=["people"]) 
app.include_router(image_router, prefix="/image", tags=["image"]) 

# Serve built frontend if present
DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "web", "dist"))
if os.path.isdir(DIST_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")
    app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="frontend")