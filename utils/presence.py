import time
from pypresence import Presence
from utils import get_config, log
from utils.retroachievements import get_game_icon, get_console_icon

config = get_config()

def update_rpc_client_id(new_client_id: int, RPC: Presence) -> Presence:
    if RPC and int(RPC.client_id) == int(new_client_id):
        log.debug("Client ID hasn't changed, skipping...")
        return RPC

    if RPC:
        log.debug("Closing connection with old client ID...")
        RPC.close()

    RPC = Presence(new_client_id)
    log.info("Updating client ID...")
    RPC.connect()
    log.success(f"Connected with new client ID! ({new_client_id})")
    return RPC


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
last_update_time = time.time()  # Track when data was last updated
last_state = None  # Track the last state for comparison
first_presence = True  # Flag to handle the first presence update
state_updated_once = False  # Flag to track if the state has been updated at least once

def update_presence(RPC, data, game_data):
    global actual_game_title, start_time, last_update_time, last_state, first_presence, state_updated_once
    
    presence_timeout = config.get("presence_timeout", 0)
    force_presence = config.get("force_presence", False)  # Get the force_presence flag
    current_time = time.time()
    current_state = get_state(data)
    
    # Handle first presence update
    if not force_presence:  # Skip first presence logic if force_presence is enabled
        if first_presence:
            if last_state is None:
                last_state = current_state
            if current_state and last_state and current_state != last_state:
                state_updated_once = True  # Mark state as updated only if it changed from a valid previous state
            if data.get("Status", "") == "Offline" and not state_updated_once:
                log.debug("First presence is offline and state hasn't been updated, skipping...")
                return
            if not state_updated_once and data.get("Status", "") == "Offline":
                return  # Wait for a valid state update
            first_presence = False  # Allow updates after the first valid state
    
    # Check if timeout has been reached
    if not force_presence and presence_timeout > 0 and (current_time - last_update_time) > presence_timeout:
        if current_state == last_state:
            log.debug(f"No status update in {presence_timeout} seconds, clearing presence...")
            RPC.clear()
            return
    
    # Update start_time if the user changed game
    if game_data['GameTitle'] != actual_game_title:
        actual_game_title = game_data['GameTitle']
        start_time = time.time()
    
    year_of_release = get_release_year(game_data['Released'])
    details = f"{game_data['GameTitle']} ({year_of_release})"
    
    if not force_presence and data.get("Status", "") == "Offline" and current_state == last_state:
        log.debug("User is offline and state hasn't changed, skipping update...")
        return
    
    # Update last_update_time and last_state as we've received valid data
    last_update_time = current_time
    last_state = current_state
    
    RPC.update(
        state=current_state,
        details=details,
        start=start_time,
        large_image=get_game_icon(game_data),
        large_text=get_large_text(game_data),
        small_image=get_console_icon(game_data['ConsoleID']),
        small_text=game_data['ConsoleName'],
        buttons=[{"label": "View RA Profile", "url": f"https://retroachievements.org/user/{data.get('User', config.get('ra_username'))}"}]
    )
