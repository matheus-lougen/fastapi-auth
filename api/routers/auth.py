from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from api import security
from api.dependencies import SessionInjector
from api.models import User

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionInjector
) -> Any:
    """Authenticates a user and returns an access token.
    `POST https://localhost:8000/auth/token`
    Validates the provided credentials if sucessful returns a JWT access token for future authenticated requests.
    """
    user = await session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect credentials')

    if not security.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect password')

    access_token = security.create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
