from frangiclave.bot.templates.base import make_section, DIVIDER, IMAGE_FORMAT, \
    URL_FORMAT, get_image_if_reachable
from frangiclave.compendium.element import Element


def make_element(element: Element):
    image = get_image_if_reachable(get_element_art(element))
    image_alt = None
    if image is not None:
        image_alt = element.element_id
    decay_to = None
    if element.decay_to:
        decay_to = URL_FORMAT.format('element', element.decay_to.element_id)
    return [
        make_section('*Element: {}*'.format(URL_FORMAT.format('element', element.element_id))),
        DIVIDER,
        make_section(
            f'*_Label:_* {element.label}\n'
            f'*_Description:_* {element.description}',
            image,
            image_alt
        )
    ]


def get_element_art(element: Element):
    if element.no_art_needed:
        image_id = '_x'
    else:
        image_id = element.icon if element.icon else element.element_id
    return IMAGE_FORMAT.format(
        'icons40/aspects' if element.is_aspect else 'elementArt',
        image_id
    )
