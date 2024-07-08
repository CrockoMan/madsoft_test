import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

S3_URL = '/s3/'
MEME_URL = '/memes/'
MEME_DETAILS_URL = MEME_URL + '{meme_id}'

def test_s3_get_file(user_client):
    response = user_client.get(S3_URL)
    assert response.status_code == 200, (
        f'При корректном GET-запросе к эндпоинту `{S3_URL}` '
        'должен вернуться статус-код 200.'
    )


def test_s3_post_file(user_client):
    response = client.post(S3_URL,
                           files={"file": ("test_file.txt",
                                           '123',
                                           "text/plain")})
    assert response.status_code == 200, (
        f'При корректном GET-запросе к эндпоинту `{S3_URL}` '
        'должен вернуться статус-код 200.'
    )


def test_get_meme(user_client, meme):
    response = user_client.get(MEME_URL)
    assert response.status_code == 200, (
        f'При корректном GET-запросе к эндпоинту `{MEME_URL}` '
        'должен вернуться статус-код 200.'
    )
    assert len(response.json()) == 1, (
        f'При корректном GET-запросе к эндпоинту `{MEME_URL}` '
        'должен вернуться статус-код 200.'
    )
