from fastapi import status


def test_generate_access_token_should_return_ok(client, user):
    response = client.post('/auth/token', data={'username': user.email, 'password': user.clean_password})
    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_generate_access_token_should_return_incorret_password(client, user):
    request_json = {'username': user.email, 'password': 'wrongpassword'}
    expected_response_json = {'detail': 'Incorrect password'}
    response = client.post('/auth/token', data=request_json)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_response_json


def test_generate_access_token_should_return_incorret_email(client, user):
    request_json = {'username': 'kpaula2101@gmail.com', 'password': user.clean_password}
    expected_response_json = {'detail': 'Incorrect credentials'}
    response = client.post('/auth/token/', data=request_json)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_response_json
