from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from api import models, schemas, security
from api.database import Session, get_session

router = APIRouter(prefix='/users', tags=['users'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[schemas.User, Depends(security.get_current_user)]


@router.post('/', response_model=schemas.PublicUser, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, session: Session) -> Any:
    user = models.User(username=user.username, password=security.get_password_hash(user.password), email=user.email)

    if user.exists(session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Esse nome de usuário ou e-mail já estão em uso!'
        )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get('/', response_model=schemas.UserList, status_code=status.HTTP_200_OK)
def fetch_all_users_from_database(session: Session, skip: int = 0, limit: int = 100) -> Any:
    users = session.scalars(select(models.User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.get('/{user_id}', response_model=schemas.PublicUser, status_code=status.HTTP_302_FOUND)
def fetch_user_from_database(user_id: int, session: Session) -> Any:
    user = models.User.fetch_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@router.put('/{user_id}', response_model=schemas.PublicUser, status_code=status.HTTP_200_OK)
def update_user_info(user_id: int, user: schemas.User, session: Session, current_user: CurrentUser) -> Any:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

    current_user.username = user.username
    current_user.password = security.get_password_hash(user.password)
    current_user.email = user.email

    try:
        session.commit()
        session.refresh(current_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This username or email is alreadly in use')
    return current_user


@router.delete('/{user_id}', response_model=schemas.Message, status_code=status.HTTP_200_OK)
def delete_user_from_database(user_id: int, session: Session, current_user: CurrentUser) -> schemas.Message:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
