from glob import glob
from os.path import join, basename
from typing import Type, Iterable, Dict, Any

from frangiclave import csjson
from frangiclave.compendium.base import GameContentMixin, get_session
from frangiclave.compendium.deck import Deck
from frangiclave.compendium.file import File, FileCategory


def import_game_data(content_dir: str):
    with get_session() as session:
        decks = _load_content(Deck, content_dir, FileCategory.DECKS)
        session.add_all(decks)


def _load_content(
        content_class: Type[GameContentMixin],
        content_dir: str,
        category: FileCategory
):
    content = []
    for file_name, file_data in _load_json_data(join(content_dir, category.value)):
        file = File(category, file_name)
        for data in file_data[category.value]:
            content.append(content_class.from_data(file, data))
    return content


def _load_json_data(category_dir: str) -> Iterable[Dict[str, Any]]:
    for json_file_path in glob(join(category_dir, '*.json')):
        with open(json_file_path, 'r') as f:
            yield basename(json_file_path), csjson.load(f)
