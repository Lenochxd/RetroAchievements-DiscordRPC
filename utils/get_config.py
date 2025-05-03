import os
import yaml


config_path = 'config.yml'

def get_config() -> dict:
    config = None
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
    
    return config if config else {}

def get_config_full_path() -> str:
    return os.path.abspath(config_path)
