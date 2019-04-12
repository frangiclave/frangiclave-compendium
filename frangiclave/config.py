import toml

DEFAULT_CONFIG_FILE_NAME = 'config.toml'


def load_config(config_file_name):
    with open(config_file_name) as config_file:
        return toml.load(config_file)
