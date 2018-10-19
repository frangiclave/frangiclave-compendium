import io
import logging
from glob import glob
from os.path import join, basename
from typing import Type, Iterable, Dict, Any, List, Tuple

from frangiclave import csjson
from frangiclave.compendium.base import get_session, Base
from frangiclave.compendium.deck import Deck
from frangiclave.compendium.element import Element
from frangiclave.compendium.file import File, FileCategory, FileGroup
from frangiclave.compendium.game_content import GameContentMixin, GameContents
from frangiclave.compendium.legacy import Legacy

from frangiclave.compendium.recipe import Recipe
from frangiclave.compendium.verb import Verb


def import_game_data(game_dir: str):
    assets_dir = join(game_dir, 'cultistsimulator_Data', 'StreamingAssets')
    content_dir = join(assets_dir, 'content')
    with get_session() as session:
        game_contents = GameContents()
        for group in FileGroup:
            decks = _load_content(
                Deck,
                content_dir,
                group,
                FileCategory.DECKS,
                game_contents
            )
            elements = _load_content(
                Element,
                content_dir,
                group,
                FileCategory.ELEMENTS,
                game_contents
            )
            legacies = _load_content(
                Legacy,
                content_dir,
                group,
                FileCategory.LEGACIES,
                game_contents
            )
            recipes = _load_content(
                Recipe,
                content_dir,
                group,
                FileCategory.RECIPES,
                game_contents
            )
            verbs = _load_content(
                Verb,
                content_dir,
                group,
                FileCategory.VERBS,
                game_contents
            )

            # Create the dynamically generated secondary tables
            Base.metadata.create_all()

            session.add_all(decks)
            session.add_all(elements)
            session.add_all(legacies)
            session.add_all(recipes)
            session.add_all(verbs)


def _load_content(
        content_class: Type[GameContentMixin],
        content_dir: str,
        group: FileGroup,
        category: FileCategory,
        game_contents: GameContents
) -> List[GameContentMixin]:
    content = []
    for file_name, file_data in _load_json_data(
            join(content_dir, group.value, category.value)
    ):
        file = File(category, group, file_name)
        for data in file_data[category.value]:
            content.append(content_class.from_data(file, data, game_contents))
    return content


def _load_json_data(category_dir: str) -> Iterable[Tuple[str, Dict[str, Any]]]:
    for json_file_path in glob(join(category_dir, '*.json')):
        with io.open(json_file_path, 'r', encoding='utf-8') as f:
            yield basename(json_file_path), csjson.load(f)
