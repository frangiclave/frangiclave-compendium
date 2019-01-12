from typing import TYPE_CHECKING, Any, Dict

from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from frangiclave.compendium.game_content import GameContents
from frangiclave.compendium.utils import get, to_bool


if TYPE_CHECKING:
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
            game_contents: GameContents
    ) -> 'LinkedRecipeDetails':
        lr = cls()
        lr.recipe = game_contents.get_recipe(data['id'])
        lr.chance = int(data['chance']) if 'chance' in data else 100
        lr.additional = get(data, 'additional', False, to_bool)
        return lr
