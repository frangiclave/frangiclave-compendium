import time
import traceback
from typing import Any, Dict, List, Optional

from slackclient import SlackClient

from frangiclave.bot.templates.deck import make_deck
from frangiclave.bot.templates.element import make_element
from frangiclave.bot.templates.ending import make_ending
from frangiclave.bot.templates.legacy import make_legacy
from frangiclave.bot.templates.recipe import make_recipe
from frangiclave.bot.templates.verb import make_verb
from frangiclave.bot.templates.search_results import make_search_results
from frangiclave.compendium.base import get_session
from frangiclave.compendium.deck import Deck
from frangiclave.compendium.element import Element
from frangiclave.compendium.ending import Ending
from frangiclave.compendium.legacy import Legacy
from frangiclave.compendium.recipe import Recipe
from frangiclave.compendium.verb import Verb
from frangiclave.search import search_compendium, search_compendium_by_id

RTM_READ_DELAY = 0.5
PROFILE_PICTURE = \
    'https://www.frangiclave.net/static/images/elementArt/toolknockf.png'


class BotClient:

    def __init__(self, slack_bot_token: str):
        self.slack_client = SlackClient(slack_bot_token)
        connected = self.slack_client.rtm_connect(auto_reconnect=True)
        if not connected:
            raise Exception('Failed to connect to Slack workspace')
        self.bot_id = self.slack_client.api_call('auth.test')['user_id']

    def process_event(
            self,
            event: Dict[str, Any]
    ):
        if 'bot_id' in event and event['bot_id'] == self.bot_id:
            return
        if event['type'] == 'message':
            if 'subtype' in event and event['subtype'] in (
                    'bot_message', 'message_changed'
            ):
                return
            text = event['text']
            if text.startswith('?'):
                bits = text.split(maxsplit=1)
                command = bits[0][1:]
                params = bits[1] if len(bits) > 1 else None
                self.process_command(event, command, params)

    def process_command(
            self,
            event: Dict[str, Any],
            command: str,
            params: str
    ):
        if command in ('', 'g', 'get'):
            with get_session() as session:
                result = search_compendium_by_id(session, params.strip())
                if not result:
                    self.reply(event, 'No results found.')
                elif isinstance(result, Deck):
                    self.reply(event, None, make_deck(result))
                elif isinstance(result, Element):
                    self.reply(event, None, make_element(result))
                elif isinstance(result, Legacy):
                    self.reply(event, None, make_legacy(result))
                elif isinstance(result, Recipe):
                    self.reply(event, None, make_recipe(result))
                elif isinstance(result, Verb):
                    self.reply(event, None, make_verb(result))
                elif isinstance(result, Ending):
                    self.reply(event, None, make_ending(result))
        elif command in ('s', 'search'):
            keywords = params.strip()
            with get_session() as session:
                results = search_compendium(session, keywords)
            self.reply(event, None, make_search_results(keywords, results))

    def reply(
            self,
            event: Dict[str, Any],
            text: Optional[str] = None,
            blocks: List[Dict[str, Any]] = None
    ):
        result = self.slack_client.api_call(
            'chat.postMessage',
            channel=event['channel'],
            text=text,
            icon_url=PROFILE_PICTURE,
            thread_ts=event['thread_ts'] if 'thread_ts' in event else None,
            blocks=blocks
        )
        if not result['ok']:
            print('Failed to reply: {}'.format(result))

    def run(self):
        while self.slack_client.server.connected:
            events = self.slack_client.rtm_read()
            for event in events:
                # noinspection PyBroadException
                try:
                    self.process_event(event)
                except:
                    print('Failed to process event:', event)
                    traceback.print_exc()
            time.sleep(RTM_READ_DELAY)
