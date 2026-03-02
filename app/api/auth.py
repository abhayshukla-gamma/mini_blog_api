from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token, decode_access_token
from app.core.security import hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserLogin, UserRegister

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="email already registered ")

    hashed_password = hash_password(user.password)

    new_user = User(email=user.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "user registered successfully "}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):  # fastapi inbuilt form handler

    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="invalid email")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="invalid password")

    access_token = create_access_token(data={"sub": str(db_user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


# from fastapi import Depends, HTTPException
# from app.core.jwt import decode_access_token

# @router.get("/profile")
# def get_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

#     # Step 1: Verify JWT token
#     payload = decode_access_token(token)

#     if payload is None:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")

#     # Step 2: Fetch user using user_id (payload)
#     user_id = payload["sub"]
#     user = db.query(User).filter(User.id == user_id).first()

#     return {"email": user.email, "is_active": user.is_active}
