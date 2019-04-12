from frangiclave.bot.templates.base import make_section, DIVIDER, IMAGE_FORMAT, \
    URL_FORMAT, get_image_if_reachable
from frangiclave.compendium.verb import Verb


def make_verb(verb: Verb):
    image = get_image_if_reachable(get_verb_art(verb))
    image_alt = None
    if image is not None:
        image_alt = verb.verb_id
    return [
        make_section('*verb: {}*'.format(URL_FORMAT.format('verb', verb.verb_id))),
        DIVIDER,
        make_section(
            f'*_Label:_* {verb.label}\n'
            f'*_Description:_* {verb.description}',
            image,
            image_alt
        )
    ]


def get_verb_art(verb: Verb):
    return IMAGE_FORMAT.format('icons100/verbs', verb.verb_id)
