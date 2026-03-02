from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import (  # CryptContext ye ek clas hai passlib library ka dcide karti hai konsa algo use hoga hashing ke liye
    CryptContext,
)
from sqlalchemy.orm import Session

# from app.api.blog import oauth2_scheme
from app.core.jwt import decode_access_token
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)  # builtin security helper fetch the token from the authorization header


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    payload = decode_access_token(token)  #  ye token ko decode karega

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid or expired token ")

    user_id = payload.get("sub")  # this will give the id

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise HTTPException(status_code=401, detail="user not found")

    return user


pwd_context = CryptContext(
    schemes=["bcrypt"]
)  # schemes=["bcrypt"] bcrypt algo using auto salting is done
# CryptContext making configuration object and tells which algo to use


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
