import json
import os
import string
from multiprocessing import Pool
from time import sleep
from typing import Dict

from api_caller.get_card import get_card_by_name
from image_downloader.download_image import download_image


SIZE_THRESHOLD_BYTES = 1024000
CARD_DIR = '/mnt/c/Users/danny/AppData/Local/Forge/Cache/pics/cards'
IGNORE_CARDS = {
    'Plains1',
    'Island1',
    'Swamp1',
    'Mountain1'
    'Forest1',
    'Sol Ring'
}


def handle_multi_faced_cards(card_name: str, card: Dict):
    card_faces = card.get('card_faces')
    if card_faces is not None and len(card_faces) > 0:
        for f in card_faces:
            if f.get('name') == card_name:
                return f.get('image_uris').get('png')

    return ''


def download_replace_image(file_name: str):
    card_name: str = (file_name.split('.')[0]).rstrip(string.digits)
    card_size: int = os.path.getsize(file_name)
    if card_name in IGNORE_CARDS or card_size > SIZE_THRESHOLD_BYTES:
        print(f'{card_name} is ignored')
        return

    print(card_name)
    try:
        card = get_card_by_name(card_name=card_name)
    except Exception as e:
        print(f'Error requesting {card_name}: {e}')
        return

    image_uris = card.get('image_uris')
    if image_uris is None:
        png_uri = handle_multi_faced_cards(card_name=card_name, card=card)
        if '' == png_uri:
            print(f'Error downloading image for: {card_name}')
            return
    else:
        png_uri = image_uris.get('png')


    download_image(url=png_uri, destination=f'{CARD_DIR}/{file_name}')
    print(f'Downloaded image for {file_name} successfully')
    sleep(50 / 1000)


if __name__ == "__main__":
    os.chdir(CARD_DIR)
    p = Pool(8)
    p.map(download_replace_image, os.listdir())
    print('Downloads completed')
