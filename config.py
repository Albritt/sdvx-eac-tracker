import yaml

def load_config() -> dict:
    with open('config.yml') as file:
        return yaml.load(file, yaml.Loader)