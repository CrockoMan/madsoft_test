import pytest


@pytest.fixture
def meme(mixer):
    return mixer.blend(
        'app.models.meme.Meme',
        text='Text',
        file='1.jpg',
    )
