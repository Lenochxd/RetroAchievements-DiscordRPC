import requests

def get_game_icon(game_data: dict) -> str:
    game_icon = game_data.get('GameIcon') or game_data.get('ImageBoxArt')
    
    if game_icon:
        image_url = f"https://media.retroachievements.org{game_icon}"
        response = requests.head(image_url)
        if response.status_code == 200:
            return image_url
    
    return "ra_logo"
