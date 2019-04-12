from frangiclave.compendium.base import Base
from frangiclave.config import DEFAULT_CONFIG_FILE_NAME, load_config
from frangiclave.server import app


def init_db():
    # Load all the models
    # noinspection PyUnresolvedReferences
    from frangiclave.compendium import deck, element, file, legacy, recipe, verb

    # Create the database tables
    Base.metadata.create_all()


def init():
    # Load the configuration
    config = load_config(DEFAULT_CONFIG_FILE_NAME)

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
