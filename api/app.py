from typing import Any

from fastapi import FastAPI, status

from api import schemas

app = FastAPI()


@app.get('/', response_model=schemas.Message, status_code=status.HTTP_200_OK)
def root() -> Any:
    return {'message': 'Hello World'}
