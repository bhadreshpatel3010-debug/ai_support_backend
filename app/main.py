from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import init_db, get_db
from app.models import User
from app.schemas import UserCreate, Token, IngestRequest, ChatRequest, ChatResponse
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.rag_service import ingest_document, generate_support_reply


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Initialize the database and create tables
    yield  # This is where the application runs, and cleanup can be done after this point

app = FastAPI(title="AI Customer Support Backend", lifespan=lifespan)

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/ingest")
def ingest_knowledge(
    payload: IngestRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    count = ingest_document(payload.text, db)
    return {"message": f"Successfully stored {count} document chunks"}

@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    reply = generate_support_reply(current_user.id, request.message, db)
    return ChatResponse(reply=reply)


