from app.core.config import settings


def meme_with_path(meme, add_id=False):
    if add_id:
        return {
            'id': meme.id,
            'text': meme.text,
            'file': f'{settings.s3_bucket_public_path}{meme.file}'
        }

    return {
        'text': meme.text,
        'file': f'{settings.s3_bucket_public_path}{meme.file}'
    }
