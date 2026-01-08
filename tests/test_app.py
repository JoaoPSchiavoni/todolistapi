from http import HTTPStatus

from fastapi.testclient import TestClient

from todolist_api.app import app

client = TestClient(app)


def test_root_deve_retornar_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Ola mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_olamundogtml_deve_retornar_200():
    client = TestClient(app)

    response = client.get('/ex')

    assert response.status_code == HTTPStatus.OK
