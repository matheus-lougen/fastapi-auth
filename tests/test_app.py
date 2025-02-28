from fastapi import status


def test_root_should_return_ok_and_message(client):
    """Tests getting the message in the root route of the application.
    `GET https://localhost:8000/`
    Ensures the HTTP response has a 200 (OK) status code,
    and the content returned is a JSON object containing the message 'Hello World'.
    """
    expected_response_json = {'message': 'Hello World'}
    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response_json
