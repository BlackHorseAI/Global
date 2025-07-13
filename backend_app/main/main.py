from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database.database import get_db
from .api.v1 import agents # Simplified router import
from .security_manager import verify_password, create_access_token
from .schemas import Token, UserCreate, UserInDB
from .core.user_manager import create_user, get_user_by_username
from pydantic import BaseModel

app = FastAPI(title="The Global Payment Network Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])

class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/token", response_model=Token)
async def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=UserInDB)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return create_user(db=db, user=user_in)