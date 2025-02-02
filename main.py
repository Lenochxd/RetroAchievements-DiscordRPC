from pypresence import Presence 
import time
from utils import get_config, log, parse_args, get_arg, update_presence
from utils.retroachievements import get_profile_data, get_game_data

parse_args()


def main():
    config = get_config()
    
    username = config.get('ra_username')
    api_key = config.get('ra_api_key')
    client_id = config.get('discord_client_id')
    if client_id == "-1" or not config.has_option('client_id'):
        client_id = "1249693940299333642"

    profile_url = f"https://retroachievements.org/API/API_GetUserProfile.php?u={username}&y={api_key}&z={username}"

    start_time = int(time.time())

    RPC = Presence(client_id)
    log.info("Connecting to Discord App...")
    RPC.connect()
    log.success("Connected!")

    while True:
        data = get_profile_data(profile_url)
        game_data = get_game_data(username, data.get('LastGameID'), api_key)
        if not data or not game_data:
            log.warning("Failed to retrieve data...")
            break

        log.debug(f"RichPresenceMsg: {data['RichPresenceMsg']}")
        log.debug(f"Game Title: {game_data['GameTitle']}")
        log.debug(f"Game data: {game_data}")

        update_presence(RPC, data, game_data, start_time)

        log.debug(f"Sleeping for {get_arg('fetch')} seconds...")
        time.sleep(get_arg("fetch"))

if __name__ == "__main__":
    main()