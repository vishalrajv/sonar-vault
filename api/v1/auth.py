from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
from database.db import get_db
from models.user import User
from app.schemas import UserLogin, Token
from app.auth_utils import verify_password
from app.token_utils import create_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api/v1", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

# Define expiration for Remember Me (e.g., 7 days)
REMEMBER_ME_EXPIRE_DAYS = 7

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        jti: str = payload.get("jti")
        if username is None or jti is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
        
    # Concurrency check: Verify that the token's JTI matches the one in the DB
    if user.current_session_id != jti:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session invalidated by another login",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user

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

    # Determine token expiration
    if user_credentials.remember_me:
        expires_delta = timedelta(days=REMEMBER_ME_EXPIRE_DAYS)
    else:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token, jti = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=expires_delta
    )
    
    # Update current_session_id for concurrency control
    user.current_session_id = jti
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Logs out the user by clearing the current_session_id in the DB."""
    current_user.current_session_id = None
    db.commit()
    return {"detail": "Successfully logged out"}

@router.get("/session/status")
def get_session_status(current_user: User = Depends(get_current_user)):
    """Returns the current user info if the session is valid."""
    return {
        "username": current_user.username,
        "role": current_user.role,
        "is_active": current_user.is_active
    }
