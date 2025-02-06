import jwt

from api import security


def test_jwt():
    data = {'test': 'test'}
    token = security.create_access_token(data)

    decoded = jwt.decode(token, security.SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_password_hash():
    password = 'password123'
    hashed_password = security.get_password_hash(password)
    assert security.verify_password(password, hashed_password)
