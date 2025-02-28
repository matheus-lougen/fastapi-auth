from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api import models, security
from api.database import Session, get_session

router = APIRouter(prefix='/auth', tags=['auth'])
Session = Annotated[Session, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', status_code=status.HTTP_200_OK)
def login_for_access_token(form_data: OAuth2Form, session: Session) -> Any:
    user = models.User.fetch_by_email(form_data.username, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email')

    if not security.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect password')

    access_token = security.create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
