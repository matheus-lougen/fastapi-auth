from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api import database, schemas, security

SessionInjector = Annotated[AsyncSession, Depends(database.get_session)]
CurrentUserInjector = Annotated[schemas.User, Depends(security.get_current_user)]
