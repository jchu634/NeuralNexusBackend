from sqlalchemy.orm import Session
from requests import Response
from time import time
from passlib.hash import argon2
import uuid

from library.database import models
from library.config import Settings

#### Images ####


def create_image(db: Session, image_hash: str, image_name: str, uid: str):
    user = get_user_by_uid(uid)
    db_image = models.Image(id=uuid.uuid4().hex, image_hash=image_hash,
                            image_name=image_name, uid=uid, user=user, expiry_time=time.time()+user.settings.image_expiry)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


#### Settings ####


def get_settings_by_uid(db: Session, uid: str):
    return db.query(models.Setting).filter(models.Setting.id == uid).first()


def get_image_expiry_by_uid(db: Session, uid: str, new_expiry: int):
    db_settings = get_settings_by_uid(db, uid)
    return db_settings.image_expiry


def update_image_expiry_by_uid(db: Session, uid: str, new_expiry: int):
    db_settings = get_settings_by_uid(db, uid)
    db_settings.image_expiry = new_expiry
    db.commit()
    db.refresh(db_settings)
    return db_settings

#### Users ####


def get_user_by_uid(db: Session, uid: str):
    return db.query(models.User).filter(models.User.id == uid).first()


def get_users_by_username(db: Session, name: str):
    return db.query(models.User).filter(models.User.username == name).first()


def get_users_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, username: str, email: str, password: str):
    db_settings = models.Setting(
        id=uuid.uuid4().hex, image_expiry=Settings.IMAGE_DEFAULT_EXPIRY_PERIOD)
    db_user = models.User(id=db_settings.id, username=username,
                          email=email, password_hash=argon2.hash(password), is_admin=False)
    db_settings.user = db_user

    db.add(db_user)
    db.add(db_settings)

    db.commit()
    db.refresh(db_user)
    db.refresh(db_settings)
    return db_user


def update_user_email(db: Session, username: str, email: str):
    db_user = get_users_by_username(username)
    db_user.email = email
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(db: Session, username: str, password: str):
    db_user = get_users_by_username(username)
    db_user.password = argon2.hash(password)
    db.commit()
    db.refresh(db_user)
    return db_user
