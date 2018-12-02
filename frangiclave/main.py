import toml

from frangiclave.compendium.base import Base
from frangiclave.server import app

CONFIG_FILE_NAME = 'config.toml'


def load_config(config_file_name):
    with open(config_file_name) as config_file:
        return toml.load(config_file)


def init_db():
    # Load all the models
    # noinspection PyUnresolvedReferences
    from frangiclave.compendium import deck, element, file, legacy, recipe, verb

    # Create the database tables
    Base.metadata.create_all()


def init():
    # Load the configuration
    config = load_config(CONFIG_FILE_NAME)

    # Initialize the database connection
    init_db()

    # Set the global variables
    app.config.update(config['frangiclave'])

    return app


def main():
    # Run the app
    app.run()


init()

if __name__ == '__main__':
    main()
