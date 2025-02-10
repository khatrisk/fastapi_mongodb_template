from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from mongodb.db import init_db
from routes.user_routes import user_route
from routes.token_route import token_route
from models.message_models import Message


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
def root() -> Message:
    """Route is point of entry and publicly accessible"""
    welcome_message = Message(
        message="""Welcome to my FastApi boilerplate api. To view and use the routes, 
        add '/docs' to the path that brought you to this page."""
    )
    return welcome_message


app.include_router(user_route, prefix="/user", tags=["users"])
app.include_router(token_route, tags=["token"])

@app.on_event("startup")
async def connect():
    await init_db()


if __name__ == "__main__":
    uvicorn.run(reload=True, app="server:app")
