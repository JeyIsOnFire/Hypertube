# api-gateway/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routers import users, movies



app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4000", # permet de faire fonctionner le cors pour nextjs voir si on peut suppr a l'avenir
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api")
app.include_router(movies.router, prefix="/api")
# app.include_router(stream.router, prefix="/api")
# app.include_router(oauth.router, prefix="/api")
