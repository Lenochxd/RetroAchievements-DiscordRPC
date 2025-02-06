import time
import threading
from pypresence import Presence 
from utils import get_config, log, parse_args, get_arg, update_presence
from utils.retroachievements import get_profile_data, get_game_data

parse_args()
config = get_config()


def initialize_tray_icon():
    from tray import create_tray_icon
    try:
        create_tray_icon()
    except Exception as e:
        log.exception(e, "Failed to initialize tray icon", expected=False)

def main():
    username = config.get('ra_username')
    api_key = config.get('ra_api_key')
    client_id = config.get('discord_client_id')
    if not client_id or client_id == "-1":
        client_id = "1249693940299333642"

    RPC = Presence(client_id)
    log.info("Connecting to Discord App...")
    RPC.connect()
    log.success("Connected!")

    while True:
        data = get_profile_data(username, api_key)
        game_data = get_game_data(username, data.get('LastGameID'), api_key)
        if not data or not game_data:
            log.warning("Failed to retrieve data...")
            break

        log.debug(f"RichPresenceMsg: {data['RichPresenceMsg']}")
        log.debug(f"Game Title: {game_data['GameTitle']}")
        log.debug(f"Game data: {game_data}")

        update_presence(RPC, data, game_data)

        log.debug(f"Sleeping for {get_arg('fetch')} seconds...")
        time.sleep(get_arg("fetch"))

if __name__ == "__main__":
    # Start the RPC thread
    rpc_thread = threading.Thread(target=main, daemon=True)
    rpc_thread.start()
    
    # Start the tray icon
    initialize_tray_icon()
