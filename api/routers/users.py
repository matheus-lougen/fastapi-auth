from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import exists, select
from sqlalchemy.exc import IntegrityError

from api import models, schemas, security
from api.dependencies import CurrentUserInjector, SessionInjector

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=schemas.PublicUser, status_code=status.HTTP_201_CREATED)
async def create_new_user(user_data: schemas.User, session: SessionInjector) -> Any:
    hashed_password = security.get_password_hash(user_data.password)
    user = models.User(username=user_data.username, password=hashed_password, email=user_data.email)

    if await session.scalar(
        exists().where((models.User.username == user.username) | (models.User.email == user.email)).select()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Esse nome de usuário ou e-mail já estão em uso!'
        )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@router.get('/', response_model=schemas.UserList, status_code=status.HTTP_200_OK)
async def get_users_list(session: SessionInjector, skip: int = 0, limit: int = 100) -> Any:
    query = await session.scalars(select(models.User).offset(skip).limit(limit))
    users = query.all()
    return {'users': users}


@router.get('/{user_id}', response_model=schemas.PublicUser, status_code=status.HTTP_302_FOUND)
async def get_user_by_id(user_id: int, session: SessionInjector) -> Any:
    user = await session.scalar(select(models.User).where(models.User.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@router.put('/{user_id}', response_model=schemas.PublicUser, status_code=status.HTTP_200_OK)
async def update_user_info(
    user_id: int, user: schemas.User, session: SessionInjector, current_user: CurrentUserInjector
) -> Any:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

    current_user.username = user.username
    current_user.password = security.get_password_hash(user.password)
    current_user.email = user.email

    try:
        await session.commit()
        await session.refresh(current_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This username or email is alreadly in use')
    return current_user


@router.delete('/{user_id}', response_model=schemas.Message, status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, session: SessionInjector, current_user: CurrentUserInjector) -> Any:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions')

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}
