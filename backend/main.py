from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI(title="FastAPI + React")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/hello")
def hello(name: str = "World") -> dict[str, str]:
    return {"message": f"Hello, {name}!"}


class User(BaseModel):
    id: int
    name: str
    email: EmailStr  # invalid emails get a 422 response automatically


@app.post("/api/user")
def create_user(user: User) -> dict[str, str]:
    return {
        "message": f"Hello {user.name} (ID {user.id}), we'll email you at {user.email}."
    }


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

# dist/ only exists after `npm run build`; in dev the Vite server serves the UI.
if FRONTEND_DIR.is_dir():
    app.frontend("/", directory=FRONTEND_DIR)