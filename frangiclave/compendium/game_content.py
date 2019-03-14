from typing import Any, Dict

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from frangiclave.compendium.file import File


class GameContents:

    def __init__(self):
        self.decks = {}
        self.elements = {}
        self.legacies = {}
        self.recipes = {}
        self.verbs = {}
        self.endings = {}

    def get_deck(self, deck_id):
        if not deck_id:
            return None
        if deck_id in self.decks:
            return self.decks[deck_id]
        from frangiclave.compendium.deck import Deck
        self.decks[deck_id] = Deck(deck_id=deck_id)
        return self.decks[deck_id]

    def get_element(self, element_id):
        if not element_id:
            return None
        if element_id in self.elements:
            return self.elements[element_id]
        from frangiclave.compendium.element import Element
        self.elements[element_id] = Element(element_id=element_id)
        return self.elements[element_id]

    def get_legacy(self, legacy_id):
        if not legacy_id:
            return None
        if legacy_id in self.legacies:
            return self.legacies[legacy_id]
        from frangiclave.compendium.legacy import Legacy
        self.legacies[legacy_id] = Legacy(legacy_id=legacy_id)
        return self.legacies[legacy_id]

    def get_recipe(self, recipe_id):
        if not recipe_id:
            return None
        if recipe_id in self.recipes:
            return self.recipes[recipe_id]
        from frangiclave.compendium.recipe import Recipe
        self.recipes[recipe_id] = Recipe(recipe_id=recipe_id)
        return self.recipes[recipe_id]

    def get_verb(self, verb_id):
        if not verb_id:
            return None
        if verb_id in self.verbs:
            return self.verbs[verb_id]
        from frangiclave.compendium.verb import Verb
        self.verbs[verb_id] = Verb(verb_id=verb_id)
        return self.verbs[verb_id]

    def get_ending(self, ending_id):
        if not ending_id:
            return None
        if ending_id in self.endings:
            return self.endings[ending_id]
        from frangiclave.compendium.ending import Ending
        self.endings[ending_id] = Ending(ending_id=ending_id)
        return self.endings[ending_id]


class GameContentMixin:

    @declared_attr
    def file_id(self) -> Column:
        return Column(Integer, ForeignKey(File.id))

    @declared_attr
    def file(self) -> File:
        return relationship(File)

    @classmethod
    def from_data(
            cls,
            file: File,
            data: Dict[str, Any],
            game_contents: GameContents
    ):
        raise NotImplementedError
