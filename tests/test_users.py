from fastapi import status

from api import schemas, security


def create_new_user_should_return_created_and_public_user_json(client):
    """Tests creating a new user in the application.
    `POST https://localhost:8000/users/`
    Ensures the HTTP response has a 201 (CREATED) status code,
    and the content returned is a JSON object containing the public data of the created user.
    """
    request_json = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'mynewpassword',
    }
    expected_response_json = {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }
    response = client.post('/users/', json=request_json)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response_json


def test_create_user_should_return_bad_request_and_message(client, user):
    """Tests creating a new user in the application.
    `POST https://localhost:8000/users/`
    Ensures the HTTP response has a 201 (CREATED) status code,
    and the content returned is a JSON object containing the public data of the created user.
    """
    request_json = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'mynewpassword',
    }
    expected_response_json = {'detail': 'Esse nome de usuário ou e-mail já estão em uso!'}
    response = client.post('/users/', json=request_json)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_response_json


def test_get_users_should_return_ok_and_empty_list_of_users(client):
    """Tests getting a list of the application users with no users in the database.
    `GET https://localhost:8000/users/`
    Ensures the HTTP response has a 200 (OK) status code,
    and the content returned is a JSON object containing a empty list.
    """
    expected_response_json = {'users': []}
    response = client.get('/users/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response_json


def test_get_users_should_return_ok_and_list_of_stored_users(client, user):
    """Test getting a list of the application users with users in the database.
    `GET https://localhost:8000/users/`
    Ensures the HTTP response has a 200 (OK) status code,
    and the content returned is a JSON object containing a list of public user data.
    """
    public_user_json = schemas.PublicUser(username=user.username, email=user.email, id=user.id).model_dump()
    expected_response_json = {'users': [public_user_json]}
    response = client.get('/users/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response_json


def test_get_user_should_return_not_found_and_message(client):
    """Test getting a user by an id that doesn't exists.
    `GET https://localhost:8000/users/{user_id}`
    Ensures the HTTP response has a 404 (NOT FOUND) status code,
    and the content returned is a JSON object containing a 'User not found' message.
    """
    expected_response_json = {'detail': 'User not found'}
    response = client.get('/users/999')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == expected_response_json


def test_get_user_should_return_ok_and_stored_user(client, user):
    """Test getting a user by an id that exists.
    `GET https://localhost:8000/users/{user_id}`
    Ensures the HTTP response has a 302 (FOUND) status code,
    and the content returned is a JSON object containing the user public data.
    """
    expected_response_json = {'username': 'bob', 'email': 'bob@example.com', 'id': 1}
    response = client.get('/users/1')

    assert response.status_code == status.HTTP_302_FOUND
    assert response.json() == expected_response_json


def test_update_user_should_return_ok_and_stored_user(client, user, token):
    """Test updating the username, email and password of a user that exists.
    `GET https://localhost:8000/users/{user_id}`
    Ensures the HTTP response has a 200 (OK) status code,
    and the content returned is a JSON object containing the user updated public data.
    """
    request_json = {
        'username': 'john',
        'email': 'john@example.com',
        'password': 'johnnewpassword',
    }
    expected_response_json = {
        'username': 'john',
        'email': 'john@example.com',
        'id': 1,
    }
    response = client.put(f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}, json=request_json)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response_json


def test_update_user_while_not_authorized(client, user, token):
    """Test updating the email of a user while not authorized to do so.
    `GET https://localhost:8000/users/{user_id}`
    Ensures the HTTP response has a 200 (OK) status code,
    and the content returned is a JSON object containing the user updated public data.
    """
    request_json = {
        'username': 'john',
        'email': 'john@example.com',
        'password': 'johnnewpassword',
    }
    expected_response_json = {'detail': 'Not enough permissions'}
    response = client.put('/users/9999', headers={'Authorization': f'Bearer {token}'}, json=request_json)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == expected_response_json


def test_update_user_should_return_conflict_and_message(client, user, token):
    """Test updating the username and email of a user to one that is alreadly in use.
    `PUT https://localhost:8000/users/{user_id}`
    Ensures the HTTP response has a 409 (CONFLICT) status code,
    and the content returned is a JSON object containing a error message.
    """
    request_json = {
        'username': 'john',
        'email': 'john@example.com',
        'password': 'johnnewpassword',
    }
    expected_response_json = {'detail': 'This username or email is alreadly in use'}
    client.post('/users/', json=request_json)
    response = client.put(f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}, json=request_json)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == expected_response_json


def test_delete_user_should_return_ok_and_message(client, user, token):
    """Test deleting a user by an id that exists.
    `DELETE https://localhost:8000/users/{user_id}`
    Ensures the HTTP response has a 200 (OK) status code,
    and the content returned is a JSON object containing a confirmation message.
    """
    response = client.delete('/users/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_while_not_authorized(client, user, token):
    """Test deleting a user without authorized.
    `DELETE https://localhost:8000/users/{user_id}`
    Ensures the HTTP response has a 401 (UNAUTHORIZED) status code,
    and the content returned is a JSON object containing a error message.
    """
    response = client.delete('/users/8260382490', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_while_not_authenticated(client):
    """Test deleting a user without authorized.
    `DELETE https://localhost:8000/users/{user_id}`
    Ensures the HTTP response has a 401 (UNAUTHORIZED) status code,
    and the content returned is a JSON object containing a error message.
    """
    response = client.delete('/users/8260382490')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_user_using_token_with_invalid_email(client):
    data = {'no-email': 'test'}
    token = security.create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_user_using_token_with_a_email_that_dont_exists(client):
    data = {'sub': 'test@test'}
    token = security.create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
