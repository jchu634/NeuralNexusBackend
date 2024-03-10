from fastapi import APIRouter, HTTPException, status, Depends, Security, Form
from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes
from pydantic import BaseModel, ValidationError
from library.database.database import SessionLocal
from library.database import crud, models
from library.config import Settings

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from passlib.hash import argon2
from typing import Annotated
from jose import JWTError, jwt

import traceback
import logging

################ Blueprint/Namespace Configuration ################
auth_api = APIRouter(tags=["Auth"])

################ Global Variables ################
img_path = Settings.UPLOAD_FOLDER
models_path = Settings.MODEL_FOLDER
isProduction = Settings.ENV_TYPE == 'production'
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

################ Helper Functions ################

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, Settings.AUTH_SECRET_KEY, algorithm=Settings.AUTH_ALGORITHM)
    return encoded_jwt


async def get_current_user(
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(Settings.OAUTH_SCHEME)],
        db: Annotated[Session, Depends(get_db)]
):

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    try:
        payload = jwt.decode(token, Settings.AUTH_SECRET_KEY,
                             algorithms=[Settings.AUTH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        logging.debug(token_scopes)
        token_data = TokenData(scopes=token_scopes, username=username)
    except JWTError:
        raise credentials_exception

    user = crud.get_users_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return JSONResponse(content={
        "uid": user.id,
        "username": user.username,
        "email": user.email,
        "admin": user.is_admin
    })


async def get_current_active_user(current_user: Annotated[models.User, Security(get_current_user, scopes=["user"])]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def check_if_user_admin(
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(Settings.OAUTH_SCHEME)],
        db: Annotated[Session, Depends(get_db)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        logging.debug(authenticate_value)
    else:
        authenticate_value = "Bearer"
    try:
        payload = jwt.decode(token, Settings.AUTH_SECRET_KEY,
                             algorithms=[Settings.AUTH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = crud.get_users_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        logging.debug(token_data.scopes)
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user.is_admin

################ Auth ####################


@auth_api.post("/create_user")
def create_user(username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    try:
        crud.create_user(db, username, email, password)
        logging.info(f"Created user {username}")
        return JSONResponse(content={"success": "user made"})
    except IntegrityError as e:
        return ORJSONResponse(content={"error": "Username already taken"}, status_code=500)
    except Exception as e:
        logging.error(f"User creation error: {traceback.format_exc()}")
        return ORJSONResponse(content={"error": "Internal Server Error"}, status_code=500)


@auth_api.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user = crud.get_users_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        if argon2.verify(str(form_data.password), user.password_hash):
            access_token_expires = timedelta(
                minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            logging.debug(form_data.scopes)
            access_token = create_access_token(
                data={"sub": user.username, "scopes": form_data.scopes},
                expires_delta=access_token_expires
            )
            return Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        logging.error(f"Login error: {traceback.format_exc()}")
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@auth_api.get("/users/me")
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user


@auth_api.get("/read_token")
async def read_items(token: Annotated[str, Depends(Settings.OAUTH_SCHEME)]):
    return {"token": token}
