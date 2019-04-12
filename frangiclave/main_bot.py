from frangiclave.bot.client import BotClient
from frangiclave.config import DEFAULT_CONFIG_FILE_NAME, load_config


def main():
    # Load the configuration
    print('Loading configuration...')
    config = load_config(DEFAULT_CONFIG_FILE_NAME)

    # Set up the bot and keep listening for events forever
    print('Initializing bot client...')
    client = BotClient(config['frangiclave']['SLACK_BOT_TOKEN'])
    print('Bot client ready. Listening...')
    client.run()


if __name__ == '__main__':
    main()
