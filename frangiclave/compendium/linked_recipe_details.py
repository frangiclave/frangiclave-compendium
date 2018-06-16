from typing import Any, Dict, List

from frangiclave.compendium.utils import get, to_bool


class LinkedRecipeDetails:

    id: str
    chance: int
    additional: bool

    def __init__(
            self,
            _id: str,
            chance: int = '',
            additional: bool = False
    ):
        self.id = _id
        self.chance = chance
        self.additional = additional

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'LinkedRecipeDetails':
        lr = cls(data['id'], int(data['chance']))
        lr.additional = get(data, 'additional', False, to_bool)
        return lr


def to_linked_recipe_details(
        val: List[Dict[str, Any]]
) -> List['LinkedRecipeDetails']:
    return [LinkedRecipeDetails.from_data(v) for v in val]
