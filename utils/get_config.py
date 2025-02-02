import os
import yaml
from .logger import log


def setup_config():
    config_path = 'config.yml'
    if os.path.exists(config_path):
        return

    log.info("Config file not found. Running first time setup...")
    username = input("Enter RetroAchievements username: ")
    api_key = input("Enter RetroAchievements api_key: ")

    config = {
        'ra_username': username,
        'ra_api_key': api_key,
        'discord_client_id': '-1'
    }

    with open(config_path, 'w') as config_file:
        yaml.dump(config, config_file)

setup_config()


def get_config() -> dict:
    with open('config.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config
