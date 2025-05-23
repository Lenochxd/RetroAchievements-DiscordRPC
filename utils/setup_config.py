import yaml
from .get_config import get_config
from .logger import log
from .ui.prompt_window import ra_infos_prompt

config_path = 'config.yml'

def setup_config():
    config = get_config()
    if config and config.get('ra_username') and config.get('ra_api_key'):
        return

    if not config:
        config = {
            'github_repo': 'Lenochxd/RetroAchievements-DiscordRPC',
            'ra_username': "",
            'ra_api_key': "",
            'discord_client_id': '1337553980779266078', # RetroAchievements Discord App ID
            'sleeping_time': 10,
            'presence_timeout': 10 * 60, # Time in seconds to keep presence if status doesn't update
            'force_presence': False, # Force presence even if offline
        }
        
        with open(config_path, 'w') as config_file:
            yaml.dump(config, config_file)
    
    log.info("Config file not found or missing RetroAchievements infos. Running first time setup...")
    ra_infos_prompt()
    return
