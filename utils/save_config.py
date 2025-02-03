import yaml

def save_config(config: dict) -> None:
    with open('config.yml', 'w') as config_file:
        yaml.safe_dump(config, config_file)
