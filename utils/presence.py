import time
from utils import get_config
from utils.retroachievements import get_game_icon, get_console_icon

config = get_config()


def get_release_year(release_date: str) -> str:
    return release_date.split()[-1][:4]


start_time = time.time()
actual_game_title = ""
    
def update_presence(RPC, data, game_data):
    global actual_game_title, start_time
    # Update start_time if the user changed game
    if game_data['GameTitle'] != actual_game_title:
        actual_game_title = game_data['GameTitle']
        start_time = time.time()
    
    year_of_release = get_release_year(game_data['Released'])
    details = f"{game_data['GameTitle']} ({year_of_release})"
    
    RPC.update(
        state=data["RichPresenceMsg"],
        details=details,
        start=start_time,
        large_image=get_game_icon(game_data),
        large_text=f"Released {game_data['Released']}, Developed by {game_data['Developer']}, Published by {game_data['Publisher']}",
        small_image=get_console_icon(game_data['ConsoleID']),
        small_text=game_data['ConsoleName'],
        buttons=[{"label": "View RA Profile", "url": f"https://retroachievements.org/user/{data.get('User', config.get('ra_username'))}"}]
    )
