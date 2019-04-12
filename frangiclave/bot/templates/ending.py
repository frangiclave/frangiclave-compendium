from frangiclave.bot.templates.base import make_section, DIVIDER, \
    IMAGE_FORMAT, URL_FORMAT, get_image_if_reachable
from frangiclave.compendium.ending import Ending


def make_ending(ending: Ending):
    image = get_image_if_reachable(get_ending_art(ending))
    image_alt = None
    if image is not None:
        image_alt = ending.ending_id
    return [
        make_section('*ending: {}*'.format(URL_FORMAT.format('ending', ending.ending_id))),
        DIVIDER,
        make_section(
            f'*_Title:_* {ending.title}\n'
            f'*_Description:_* {ending.description}',
            image,
            image_alt
        )
    ]


def get_ending_art(ending: Ending):
    return IMAGE_FORMAT.format('endingArt', ending.image)
