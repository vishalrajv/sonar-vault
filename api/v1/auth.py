from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import User
from app.schemas import UserLogin, Token
from app.auth_utils import verify_password
from app.token_utils import create_access_token

router = APIRouter(prefix="/api/v1", tags=["auth"])

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token, jti = create_access_token(data={"sub": user.username, "role": user.role})
    
    # Update current_session_id for concurrency control
    user.current_session_id = jti
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer"}
