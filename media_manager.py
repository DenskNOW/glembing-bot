import os
import random

MEDIA_FOLDER = "media"

def get_random_media():
    files = os.listdir(MEDIA_FOLDER)
    if not files:
        return None

    chosen = random.choice(files)
    return os.path.join(MEDIA_FOLDER, chosen)