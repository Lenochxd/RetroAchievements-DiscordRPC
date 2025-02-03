import requests
from utils.get_config import get_config
from .get_data import get_http

config = get_config()
api_key = config.get('ra_api_key')
consoles = get_http(f"https://retroachievements.org/API/API_GetConsoleIDs.php?y={api_key}")


def get_game_icon(game_data: dict) -> str:
    game_icon = game_data.get('GameIcon') or game_data.get('ImageBoxArt')
    
    if game_icon:
        image_url = f"https://media.retroachievements.org{game_icon}"
        response = requests.head(image_url)
        if response.status_code == 200:
            return image_url
    
    return "ra_logo"

def get_console_icon(console_id: int) -> str:
    for i in consoles:
        if i.get("ID", -1) == console_id:
            return i.get("IconURL", "ra_logo")
    return "ra_logo"
