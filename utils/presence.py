import time
from utils import get_config, log
from utils.retroachievements import get_game_icon, get_console_icon

config = get_config()


def get_release_year(release_date: str) -> str:
    return release_date.split()[-1][:4]

def get_large_text(game_data: dict) -> str:
    parts = []
    
    if "Released" in game_data and game_data["Released"]:
        parts.append(f"Released {game_data['Released']}")
    if "Developer" in game_data and game_data["Developer"]:
        parts.append(f"Developed by {game_data['Developer']}")
    if "Publisher" in game_data and game_data["Publisher"]:
        parts.append(f"Published by {game_data['Publisher']}")
    
    return ", ".join(parts) if parts else None

def get_state(data: dict) -> str | None:
    state = data.get("RichPresenceMsg", "").strip()

    if state and not state.lower().startswith(f'playing {actual_game_title.lower()}'):
        return state
    return None


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
    
    if data.get("Status", "") == "Offline":
        log.debug("User is offline, clearing presence...")
        RPC.clear()
        return
    
    RPC.update(
        state=get_state(data),
        details=details,
        start=start_time,
        large_image=get_game_icon(game_data),
        large_text=get_large_text(game_data),
        small_image=get_console_icon(game_data['ConsoleID']),
        small_text=game_data['ConsoleName'],
        buttons=[{"label": "View RA Profile", "url": f"https://retroachievements.org/user/{data.get('User', config.get('ra_username'))}"}]
    )
