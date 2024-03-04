from sqlalchemy.orm import Session
from requests import Response
from time import time
from passlib.hash import argon2

from library.database import models, schemas

#### Users ####
def get_users_by_username(db: Session, name:str):
    return db.query(models.User).filter(models.User.username == name).first()

def get_users_by_email(db: Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, username:str, email:str, password:str):    
    db_user = models.User(username=username, email=email, password_hash=argon2.hash(password), is_admin=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_email(db:Session, username:str, email:str):
    db_user = get_users_by_username(username)
    db_user.email = email
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db:Session, username:str, password:str):
    db_user = get_users_by_username(username)
    db_user.password = argon2.hash(password)
    db.commit()
    db.refresh(db_user)
    return db_user