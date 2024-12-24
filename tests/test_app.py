from fastapi import status


def test_root_should_return_ok_and_message(client):
    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Hello World'}


def test_create_user_should_return_created_and_stored_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_get_users_should_return_ok_and_list_of_stored_users(client):
    response = client.get('/users/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'users': [
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'id': 1,
            }
        ]
    }


def test_get_user_should_return_not_found_and_message(client):
    response = client.get('/users/666')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_user_should_return_ok_and_stored_user(client):
    response = client.get('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_should_return_ok_and_stored_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_should_return_not_found_and_message(client):
    response = client.put(
        '/users/666',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_should_return_ok_and_message(client):
    response = client.delete('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_should_return_not_found(client):
    response = client.delete('/users/666')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
