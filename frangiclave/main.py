import toml as toml

from frangiclave.compendium.base import Base, engine
from frangiclave.server import app

CONFIG_FILE_NAME = 'config.toml'


def load_config(config_file_name):
    with open(config_file_name) as config_file:
        return toml.load(config_file)


def main():
    # Load the configuration
    config = load_config(CONFIG_FILE_NAME)

    # Create the database tables
    Base.metadata.create_all(engine)

    # Set the global variables
    app.config.update(config['frangiclave'])

    # Run the app
    app.run()


if __name__ == '__main__':
    main()
