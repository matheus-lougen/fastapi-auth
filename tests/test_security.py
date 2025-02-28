import jwt
from fastapi import status

from api import security
from api.settings import Settings

settings = Settings()


def test_jwt():
    data = {'test': 'test'}
    token = security.create_access_token(data)

    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_password_hash():
    password = 'password123'
    hashed_password = security.get_password_hash(password)
    assert security.verify_password(password, hashed_password)


def test_jwt_invalid_token(client):
    response = client.delete('/users/1', headers={'Authorization': 'Bearer token-invalido'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
