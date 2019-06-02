from typing import TYPE_CHECKING, Any, Dict, Type, List, Union

from sqlalchemy import Column, ForeignKey, Integer, Boolean, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from frangiclave.compendium.game_content import GameContents
from frangiclave.compendium.utils import get, to_bool


if TYPE_CHECKING:
    from frangiclave.compendium.element import Element
    from frangiclave.compendium.recipe import Recipe


class LinkedRecipeDetails:

    chance: int = Column(Integer)
    additional: bool = Column(Boolean)

    @declared_attr
    def recipe_id(self) -> Column:
        return Column(Integer, ForeignKey('recipes.id'))

    @declared_attr
    def recipe(self) -> 'Recipe':
        return relationship('Recipe', foreign_keys=self.recipe_id)

    @classmethod
    def from_data(
            cls,
            data: Dict[str, Any],
            challenge_cls: Type['LinkedRecipeChallengeRequirement'],
            game_contents: GameContents
    ) -> 'LinkedRecipeDetails':
        lr = cls()
        lr.recipe = game_contents.get_recipe(data['id'])
        lr.chance = int(data['chance']) if 'chance' in data else 100
        lr.additional = get(data, 'additional', False, to_bool)
        lr.challenges = challenge_cls.from_data(
            get(data, 'challenges', {}), game_contents
        )
        return lr


class LinkedRecipeChallengeRequirement:

    id = Column(Integer, primary_key=True)

    @declared_attr
    def element_id(self) -> Column:
        return Column(Integer, ForeignKey('elements.id'))

    @declared_attr
    def element(self) -> 'Element':
        return relationship('Element')

    convention = Column(String)

    @classmethod
    def from_data(
            cls, val: Union[str, Dict[str, str]], game_contents: GameContents
    ) -> List['LinkedRecipeChallengeRequirement']:
        return [
            cls(
                element=game_contents.get_element(element_id),
                convention=convention
            )
            for element_id, convention in val.items()
        ] if isinstance(val, dict) else [
            cls(
                element=game_contents.get_element(val),
                convention='base'
            )
        ]
