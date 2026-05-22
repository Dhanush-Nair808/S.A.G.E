from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os

os.makedirs("../data", exist_ok=True)

from database.database import SessionLocal, engine
from database.models import Review, User, Base
from services.review_service import process_review
from services.llm_service import generate_chat_response
from auth.password_handler import hash_password, verify_password
from auth.jwt_handler import create_token

Base.metadata.create_all(bind=engine)

# Auto-migrate: add satisfaction column if missing
try:
    from sqlalchemy import text
    _db_mig = SessionLocal()
    _result = _db_mig.execute(text("PRAGMA table_info(reviews)")).fetchall()
    _columns = [row[1] for row in _result]
    if "satisfaction" not in _columns:
        _db_mig.execute(text("ALTER TABLE reviews ADD COLUMN satisfaction VARCHAR"))
        _db_mig.commit()
    _db_mig.close()
except Exception as _mig_err:
    print(f"DB migration warning: {_mig_err}")

app = FastAPI(title="S.A.G.E Backend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Pydantic models ----------

class ReviewRequest(BaseModel):
    review: str
    username: str = "anonymous"

class FeedbackRequest(BaseModel):
    review_id: int
    satisfaction: str
    reason: str = None
    corrected_category: str = None

class ChatRequest(BaseModel):
    message: str

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


# ---------- Endpoints ----------

@app.get("/")
def home():
    return {"message": "S.A.G.E Backend Running"}


@app.post("/submit-review")
def submit_review(data: ReviewRequest, db: Session = Depends(get_db)):
    result = process_review(data.review)
    review = Review(
        username=data.username,
        review_text=data.review,
        category=result["category"],
        sentiment=result["sentiment"],
        ai_reply=result["reply"],
        satisfaction=None,
    )
    db.add(review)
    db.commit()
    return {
        "id": review.id,
        "category": result["category"],
        "sentiment": result["sentiment"],
        "reply": result["reply"],
    }


@app.post("/feedback")
def submit_feedback(data: FeedbackRequest, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == data.review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review.satisfaction = data.satisfaction
    if data.corrected_category:
        review.category = data.corrected_category
    db.commit()
    from ml.inference import retrain_model
    all_fb = db.query(Review).filter(
        Review.satisfaction.isnot(None), Review.category.isnot(None)
    ).all()
    retrain_model([r.review_text for r in all_fb], [r.category for r in all_fb])
    return {
        "message": "Feedback recorded & model retrained",
        "satisfaction": review.satisfaction,
        "category": review.category,
    }


@app.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(data.password)
    user = User(username=data.username, email=data.email, password=hashed)
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}


@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer", "username": user.username}


@app.get("/user-reviews/{username}")
def get_user_reviews(username: str, db: Session = Depends(get_db)):
    reviews = (
        db.query(Review)
        .filter(Review.username == username)
        .order_by(Review.id.desc())
        .all()
    )
    return [
        {
            "id": r.id, "username": r.username, "review": r.review_text,
            "category": r.category, "sentiment": r.sentiment,
            "reply": r.ai_reply, "satisfaction": r.satisfaction,
        }
        for r in reviews
    ]


@app.get("/public-reviews")
def get_public_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).order_by(Review.id.desc()).limit(20).all()
    return [
        {
            "id": r.id, "username": r.username, "review": r.review_text,
            "category": r.category, "sentiment": r.sentiment,
            "reply": r.ai_reply, "satisfaction": r.satisfaction,
        }
        for r in reviews
    ]


@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    """Chatbot endpoint — sends user message to Mistral LLM and returns reply."""
    try:
        reply = generate_chat_response(req.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))