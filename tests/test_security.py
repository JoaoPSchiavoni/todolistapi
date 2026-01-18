from http import HTTPStatus

from jwt import decode, encode

from todolist_api.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid-token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_missing_sub(client):
    data = {
        'exp': 9999999999,
        'type': 'access',
    }

    token = encode(data, SECRET_KEY, algorithm=ALGORITHM)
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    # Agora sim, deve cair no 'if not subject_email' e retornar 401
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
