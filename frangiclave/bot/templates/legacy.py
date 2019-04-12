from frangiclave.bot.templates.base import make_section, DIVIDER, IMAGE_FORMAT, \
    URL_FORMAT, get_image_if_reachable
from frangiclave.compendium.legacy import Legacy


def make_legacy(legacy: Legacy):
    image = get_image_if_reachable(get_legacy_art(legacy))
    image_alt = None
    if image is not None:
        image_alt = legacy.legacy_id
    return [
        make_section('*Legacy: {}*'.format(URL_FORMAT.format('legacy', legacy.legacy_id))),
        DIVIDER,
        make_section(
            f'*_Label:_* {legacy.label}\n'
            f'*_Description:_* {legacy.description}\n'
            f'*_Start Description:_* {legacy.start_description}',
            image,
            image_alt
        )
    ]


def get_legacy_art(legacy: Legacy):
    return IMAGE_FORMAT.format('icons100/legacies', legacy.image)
