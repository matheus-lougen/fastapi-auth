from fastapi import status


def test_generate_access_token_should_return_ok(client, user):
    response = client.post('/auth/token', data={'username': user.email, 'password': user.clean_password})
    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_generate_access_token_should_return_incorret_password(client, user):
    response = client.post('/auth/token', data={'username': user.email, 'password': 'wrongpassword'})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_generate_access_token_should_return_incorret_email(client, user):
    response = client.post('/auth/token/', data={'username': 'kpaula2101@gmail.com', 'password': user.clean_password})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
