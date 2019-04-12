from frangiclave.bot.templates.base import make_section, DIVIDER, URL_FORMAT
from frangiclave.compendium.deck import Deck


def make_deck(deck: Deck):
    draw_messages = '\n'.join(f'• <https://www.frangiclave.net/element/{dm.element.element_id}/|{dm.element.element_id}>: {dm.message}' for dm in deck.draw_messages)
    cards = '\n'.join(f'• <https://www.frangiclave.net/element/{card.element_id}/|{card.element_id}>' for card in deck.cards)
    default_card = f'<https://www.frangiclave.net/element/{deck.default_card.element_id}/|{deck.default_card.element_id}>' if deck.default_card else 'None'
    return [
        make_section('*Deck: {}*'.format(URL_FORMAT.format('deck', deck.deck_id))),
        DIVIDER,
        make_section(
            f'*_Label:_* {deck.label}\n'
            f'*_Description:_* {deck.description}\n'
            f'*_Draw Messages:_* \n{draw_messages}\n'
        )
    ]
