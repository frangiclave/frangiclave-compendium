from pathlib import Path
import platform
from typing import Type, Iterable, Dict, Any, List, Tuple

from jsom import JsomParser, ALL_WARNINGS

from frangiclave.compendium.base import get_session, Base
from frangiclave.compendium.deck import Deck
from frangiclave.compendium.element import Element
from frangiclave.compendium.ending import Ending
from frangiclave.compendium.file import File, FileCategory, FileGroup
from frangiclave.compendium.game_content import GameContentMixin, GameContents
from frangiclave.compendium.legacy import Legacy

from frangiclave.compendium.recipe import Recipe
from frangiclave.compendium.verb import Verb

DATA_DIR = (
    'cultistsimulator_Data' if platform.system() == 'Windows' else 'CS_Data'
)

ADDITIONAL_CULTURES = ('ru', 'zh-hans')

jsom = JsomParser(ignore_warnings=ALL_WARNINGS)


def import_game_data(game_dir: str):
    assets_dir = Path(game_dir)/DATA_DIR/'StreamingAssets'
    content_dir = assets_dir/'content'
    with get_session() as session:

        # Load the content from the regular files
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
            endings = _load_content(
                Ending,
                content_dir,
                group,
                FileCategory.ENDINGS,
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
            session.add_all(endings)
            session.add_all(legacies)
            session.add_all(recipes)
            session.add_all(verbs)


def _load_content(
        content_class: Type[GameContentMixin],
        content_dir: Path,
        group: FileGroup,
        category: FileCategory,
        game_contents: GameContents
) -> List[GameContentMixin]:
    content = []
    for file_name, file_data in _load_json_data(
            content_dir/group.value/category.value
    ):
        file = File(category, group, str(file_name))

        translations = {}
        for culture in ADDITIONAL_CULTURES:
            localised_path = content_dir/f'{group.value}_{culture}'/category.value/str(file_name)
            if not localised_path.exists():
                continue
            with localised_path.open(encoding='utf-8') as f:
                translations[culture] = {
                    e["id"]: e for e in jsom.load(f)[category.value]
                }

        for i, data in enumerate(file_data[category.value]):
            entity_id = data["id"]
            entity_translations = {}
            for culture, entities in translations.items():
                if entity_id in entities:
                    entity_translations[culture] = entities[entity_id]
            content.append(content_class.from_data(
                file, data, entity_translations, game_contents
            ))
    return content


def _load_json_data(
        category_dir: Path
) -> Iterable[Tuple[Path, Dict[str, Any]]]:
    for json_file_path in sorted(category_dir.glob('*.json')):
        with json_file_path.open(encoding='utf-8') as f:
            yield json_file_path.name, jsom.load(f)
