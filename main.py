from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import projects, misc
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Arka Portfolio API", version="1.0")

# CORS origins (frontend)
origins = [os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(misc.router, prefix="/api", tags=["misc"])
