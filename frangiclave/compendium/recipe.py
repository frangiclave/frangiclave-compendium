from typing import Any, Dict, List, Optional

from frangiclave.compendium.linked_recipe_details import \
    to_linked_recipe_details, LinkedRecipeDetails
from frangiclave.compendium.slot_specification import to_slot_specifications, \
    SlotSpecification
from frangiclave.compendium.utils import to_bool, to_int_dict, get


class Recipe:

    id: str
    label: str
    description: Optional[str]
    start_description: Optional[str]
    action_id: Optional[str]
    requirements: Dict[str, int]
    effects: Dict[str, int]
    aspects: Dict[str, int]
    craftable: bool
    hint_only: bool
    warmup: int
    aside: Optional[str]
    deck_effect: Optional[str]
    alternative_recipes: List[LinkedRecipeDetails]
    linked_recipes: List[LinkedRecipeDetails]
    ending_flag: Optional[str]
    max_executions: int
    burn_image: Optional[str]
    slot_specifications: List[SlotSpecification]

    def __init__(
            self,
            _id: str,
            label: Optional[str] = None,
            description: Optional[str] = None,
            start_description: Optional[str] = None,
            action_id: Optional[str] = None,
            requirements: Dict[str, int] = None,
            effects: Dict[str, int] = None,
            aspects: Dict[str, int] = None,
            craftable: bool = False,
            hint_only: bool = False,
            warmup: int = 0,
            aside: Optional[str] = None,
            deck_effect: Optional[str] = None,
            alternative_recipes: List[LinkedRecipeDetails] = None,
            linked_recipes: List[LinkedRecipeDetails] = None,
            ending_flag: Optional[str] = None,
            max_executions: int = 0,
            burn_image: Optional[str] = None,
            slot_specifications: List[SlotSpecification] = None
    ):
        self.id = _id
        self.label = label
        self.description = description
        self.start_description = start_description
        self.action_id = action_id
        self.requirements = requirements
        self.effects = effects if effects is not None else {}
        self.aspects = aspects if aspects is not None else {}
        self.craftable = craftable
        self.hint_only = hint_only
        self.warmup = warmup
        self.aside = aside
        self.deck_effect = deck_effect
        self.alternative_recipes = alternative_recipes\
            if alternative_recipes is not None else []
        self.linked_recipes = linked_recipes\
            if linked_recipes is not None else []
        self.ending_flag = ending_flag
        self.max_executions = max_executions
        self.burn_image = burn_image
        self.slot_specifications = slot_specifications\
            if slot_specifications is not None else []

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'Recipe':
        r = cls(data['id'])
        r.label = get(data, 'label', data['id'])
        r.description = get(data, 'description')
        r.start_description = get(data, 'startdescription')
        r.action_id = get(data, 'actionId')
        r.requirements = get(data, 'requirements', {}, to_int_dict)
        r.effects = get(data, 'effects', {}, to_int_dict)
        r.aspects = get(data, 'aspects', {}, to_int_dict)
        r.craftable = get(data, 'craftable', False, to_bool)
        r.hint_only = get(data, 'hintonly', False, to_bool)
        r.warmup = get(data, 'warmup', 0.0, int)
        r.aside = get(data, 'aside')
        r.deck_effect = get(data, 'deckeffect')
        r.alternative_recipes = get(
            data, 'alternativerecipes', [], to_linked_recipe_details
        )
        r.linked_recipes = get(data, 'linked', [], to_linked_recipe_details)
        r.ending_flag = get(data, 'ending')
        r.max_executions = get(data, 'maxexecutions', 0, int)
        r.burn_image = get(data, 'burnimage')
        r.slot_specifications = get(
            data, 'slots', [], to_slot_specifications
        )
        return r
