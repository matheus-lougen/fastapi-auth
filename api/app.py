from typing import Any

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def root() -> Any:
    return {'message': 'Hello World'}
