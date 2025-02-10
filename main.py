import time
import threading
from pypresence import Presence
from utils import get_config, log, parse_args, get_arg, update_presence
from utils.retroachievements import get_profile_data, get_game_data
from utils.presence import update_presence, update_rpc_client_id
from utils.setup_config import setup_config

parse_args()


def initialize_tray_icon():
    from tray import create_tray_icon
    try:
        create_tray_icon()
    except Exception as e:
        log.exception(e, "Failed to initialize tray icon", expected=False)

def main():
    config = get_config()
    
    username = config.get('ra_username')
    api_key = config.get('ra_api_key')
    client_id = config.get('discord_client_id', 1337553980779266078)

    RPC = Presence(client_id)
    log.info("Connecting to Discord App...")
    RPC.connect()
    log.success("Connected!")

    while True:
        config = get_config()
        username = config.get('ra_username')
        api_key = config.get('ra_api_key')
        client_id = config.get('discord_client_id', client_id)
        RPC = update_rpc_client_id(client_id, RPC)
        
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
    # Start the config setup if needed
    setup_config()
    
    # Start the RPC thread
    rpc_thread = threading.Thread(target=main, daemon=True)
    rpc_thread.start()
    
    # Start the tray icon
    initialize_tray_icon()
