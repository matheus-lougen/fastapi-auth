from fastapi import FastAPI, HTTPException, status

from api import schemas

app = FastAPI()
database = []


@app.get('/', status_code=status.HTTP_200_OK)
def root() -> schemas.Message:
    return {'message': 'Hello World'}


@app.post('/users/', status_code=status.HTTP_201_CREATED)
def post_users(user: schemas.User) -> schemas.StoredUser:
    new_user = schemas.StoredUser(**user.model_dump(), id=len(database) + 1)
    database.append(new_user)
    return new_user


@app.get('/users/', status_code=status.HTTP_200_OK)
def get_users() -> schemas.UserList:
    return {'users': database}


@app.get('/users/{user_id}')
def read_user(user_id: int) -> schemas.StoredUser:
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    return database[user_id - 1]


@app.put('/users/{user_id}')
def put_users(user_id: int, user: schemas.User) -> schemas.StoredUser:
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    user_with_id = schemas.StoredUser(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}')
def delete_user(user_id: int) -> schemas.Message:
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
