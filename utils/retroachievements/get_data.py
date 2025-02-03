import requests
from ..logger import log

def get_http(url: str) -> dict | None:
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        log.error(f"Failed to fetch data from {url}, status code: {response.status_code}")
        return None


def get_profile_data(profile_url: str) -> dict | None:
    log.debug(f"Fetching RetroAchievements activity...")
    return get_http(profile_url)

def get_game_data(username: str, game_id: str, api_key: str) -> dict | None:
    game_params = f"?z={username}&i={game_id}&y={api_key}"
    game_url = f"https://retroachievements.org/API/API_GetGame.php{game_params}"
    log.debug("Fetching game data...")
    return get_http(game_url)
