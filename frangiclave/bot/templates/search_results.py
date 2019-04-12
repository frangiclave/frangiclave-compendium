import urllib
from typing import Any, Dict, List

from frangiclave.bot.templates.base import make_section, DIVIDER, IMAGE_FORMAT, \
    URL_FORMAT, get_image_if_reachable
from frangiclave.bot.templates.element import get_element_art
from frangiclave.bot.templates.ending import get_ending_art
from frangiclave.bot.templates.legacy import get_legacy_art
from frangiclave.bot.templates.verb import get_verb_art
from frangiclave.compendium.base import get_session
from frangiclave.compendium.element import Element
from frangiclave.compendium.ending import Ending
from frangiclave.compendium.legacy import Legacy
from frangiclave.compendium.verb import Verb

MAX_RESULTS = 5


def make_search_results(keywords: str, results: List[Dict[str, Any]]):
    blocks = [
        _make_header(len(results), keywords),
    ]
    if results:
        blocks.append(DIVIDER)
        for result in results[:MAX_RESULTS]:
            blocks += [_make_result(result), DIVIDER]
    return blocks


def _make_header(num_results: int, keywords: str):
    text = 'Found *{} results* for *{}*.'.format(num_results, keywords)
    if num_results > MAX_RESULTS:
        text += ' Only showing first {} results.'.format(MAX_RESULTS)
    return make_section(text)


def _make_result(result: Dict[str, Any]):
    text = "*{}: {}*\n{}".format(
        result['type'].capitalize(),
        URL_FORMAT.format(result['type'], result['id']),
        '\n'.join('• ' + m for m in result['matches'])
    )
    image = None
    image_alt = None
    with get_session() as session:
        if result['type'] == 'element':
            element = Element.get_by_element_id(session, result['id'])
            image = get_element_art(element)
        elif result['type'] == 'legacy':
            legacy = Legacy.get_by_legacy_id(session, result['id'])
            image = get_legacy_art(legacy)
        elif result['type'] == 'verb':
            verb = Verb.get_by_verb_id(session, result['id'])
            image = get_verb_art(verb)
        elif result['type'] == 'ending':
            ending = Ending.get_by_ending_id(session, result['id'])
            image = get_ending_art(ending)

    image = get_image_if_reachable(image)
    if image is not None:
        image_alt = result['id']

    return make_section(text, image, image_alt)
