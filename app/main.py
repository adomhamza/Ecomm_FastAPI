from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, posts, auth, vote

from app.config import settings


app = FastAPI(
    title="Ecomm API",
    contact={
        "name": "Hamza Adom",
        "url": "https://linkedin.com/in/adomhamza",
        "email": "niiadom@gmail.com",
    },
)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tags_metadata = [{"name": "Post"}]


@app.get("/")
async def root():
    return {"message": "Running"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(vote.router)
app.include_router(auth.router)
