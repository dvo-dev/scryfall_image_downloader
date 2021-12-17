import json
import os
from typing import Dict

import requests

SCRYFALL_API_URL: str = 'https://api.scryfall.com'
CARD_API_URL: str = f'{SCRYFALL_API_URL}/cards'


def get_card_by_name(card_name: str) -> Dict:
    params: Dict = {'fuzzy': card_name}
    response: requests.Response = requests.get(
        f'{CARD_API_URL}/named',
        params=params
    )
    return response.json()
