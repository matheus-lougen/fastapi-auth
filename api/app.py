from fastapi import FastAPI

from api.schemas import Message

app = FastAPI()


@app.get('/')
def root() -> Message:
    return {'message': 'Hello World'}
