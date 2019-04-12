import urllib
from typing import Optional

IMAGE_FORMAT = 'https://www.frangiclave.net/static/images/{}/{}.png'
URL_FORMAT = '<https://www.frangiclave.net/{0}/{1}/|{1}>'

DIVIDER = {
    'type': 'divider'
}


def get_image_if_reachable(url: str):
    if url is None:
        return None
    try:
        urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return None
    return url


def make_section(
        text: str,
        image: Optional[str] = None,
        image_alt: Optional[str] = None):
    section = {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': text
        }
    }
    if image:
        section['accessory'] = {
            'type': 'image',
            'image_url': image
        }
        if image_alt:
            section['accessory']['alt_text'] = image_alt
    return section
