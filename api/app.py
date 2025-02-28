from typing import Any

from fastapi import FastAPI, status

from api import schemas
from api.routers import auth, users

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', response_model=schemas.Message, status_code=status.HTTP_200_OK)
def root() -> Any:
    return {'message': 'Hello World'}
