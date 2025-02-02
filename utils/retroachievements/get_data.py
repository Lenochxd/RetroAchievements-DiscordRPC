import requests
from typing import Union
from types import NoneType
from ..logger import log

def get_http(url: str) -> Union[dict, NoneType]:
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        log.error(f"Failed to fetch data from {url}, status code: {response.status_code}")
        return None


def get_profile_data(profile_url: str) -> Union[dict, NoneType]:
    log.debug(f"Fetching RetroAchievements activity...")
    return get_http(profile_url)

def get_game_data(username: str, game_id: str, api_key: str) -> Union[dict, NoneType]:
    game_params = f"?z={username}&i={game_id}&y={api_key}"
    game_url = f"https://retroachievements.org/API/API_GetGame.php{game_params}"
    log.debug("Fetching game data...")
    return get_http(game_url)
