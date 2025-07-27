from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas import TokenCreate, TokenResponse
from app.models import Token, User
from app.database import SessionLocal

SECRET_KEY = "secret"
ALGORITHM = "HS256"
router = APIRouter()
security = HTTPBearer()

@router.post("/token", response_model=TokenResponse)
def create_token(data: TokenCreate):
    db = SessionLocal()
    expires = datetime.utcnow() + timedelta(days=1)
    token_str = jwt.encode({"sub": data.username, "role": data.role}, SECRET_KEY, algorithm=ALGORITHM)
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        user = User(username=data.username, role=data.role, email="none")
        db.add(user)
        db.commit()
        db.refresh(user)
    token = Token(user_id=user.id, token=token_str, expires_at=expires)
    db.add(token)
    db.commit()
    return TokenResponse(token=token_str, expires_at=expires)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise ValueError("Missing username")
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_roles(*allowed_roles):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Allowed roles: {', '.join(allowed_roles)}"
            )
        return user
    return wrapper
