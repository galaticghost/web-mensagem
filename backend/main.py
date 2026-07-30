from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth,users
from database.database import Base, engine


app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)

Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

