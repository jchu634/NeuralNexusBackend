from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from library.database.database import SessionLocal
from library.database import crud, models
from library.config import Settings

from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError
from typing import Annotated
from pydantic import BaseModel
import traceback
import logging

################ Blueprint/Namespace Configuration ################
auth_api = APIRouter(tags=["Auth"])

################ Global Variables ################
img_path = Settings.UPLOAD_FOLDER
models_path = Settings.MODEL_FOLDER
isProduction = Settings.ENV_TYPE == 'production'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

################ Auth ####################
async def get_current_user(token: Annotated[str, Depends(Settings.OAUTH_SCHEME)], db: Annotated[Session, Depends(get_db)]):
    user = crud.get_users_by_username(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return JSONResponse(content={
        "username":user.username,
        "email":user.email
    })

async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@auth_api.get("/users/me")
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user

@auth_api.get("/items/")
async def read_items(token: Annotated[str, Depends(Settings.OAUTH_SCHEME)]):
    return {"token": token}

@auth_api.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = crud.get_users_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    ph = PasswordHasher()
    try:
        if ph.verify(user.password_hash, str(form_data.password)):
            if ph.check_needs_rehash(user.password_hash):
                crud.update_user_password(db, form_data.password)
            return {"access_token": user.username, "token_type":"bearer"}
    except InvalidHashError as e:
        logging.error(f"Login error: {traceback.format_exc()}")
        logging.debug("Invalid Hash")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    except Exception as e:
        logging.error(f"Login error: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
@auth_api.post("/create_user")
def create_user(username:str, email:str, password:str, db: Session = Depends(get_db)):
    crud.create_user(db, username,email, password)
    return JSONResponse(content={"success":"user made"})