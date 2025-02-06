from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api import models, schemas, security
from api.database import get_session

app = FastAPI()
database = []


@app.get('/', response_model=schemas.Message, status_code=status.HTTP_200_OK)
def root() -> Any:
    return {'message': 'Hello World'}


@app.post('/users/', response_model=schemas.PublicUser, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, session: Session = Depends(get_session)) -> Any:
    user = models.User(username=user.username, password=security.get_password_hash(user.password), email=user.email)

    if user.exists(session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Esse nome de usuário ou e-mail já estão em uso!'
        )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@app.get('/users/', response_model=schemas.UserList, status_code=status.HTTP_200_OK)
def fetch_all_users_from_database(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)) -> Any:
    users = session.scalars(select(models.User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.get('/users/{user_id}', response_model=schemas.PublicUser, status_code=status.HTTP_302_FOUND)
def fetch_user_from_database(user_id: int, session: Session = Depends(get_session)) -> Any:
    user = models.User.fetch_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@app.put('/users/{user_id}', response_model=schemas.PublicUser, status_code=status.HTTP_200_OK)
def update_user_info(user_id: int, user: schemas.User, session: Session = Depends(get_session)) -> Any:
    stored_user = models.User.fetch_by_id(user_id, session)

    if not stored_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    stored_user.username = user.username
    stored_user.password = security.get_password_hash(user.password)
    stored_user.email = user.email

    try:
        session.commit()
        session.refresh(stored_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This username or email is alreadly in use')
    return stored_user


@app.delete('/users/{user_id}', response_model=schemas.Message, status_code=status.HTTP_200_OK)
def delete_user_from_database(user_id: int, session: Session = Depends(get_session)) -> schemas.Message:
    user = models.User.fetch_by_id(user_id, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    session.delete(user)
    session.commit()

    return {'message': 'User deleted'}


@app.post('/token/', status_code=status.HTTP_200_OK)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)) -> Any:
    user = models.User.fetch_by_email(form_data.username, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email')

    if not security.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect password')

    access_token = security.create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
