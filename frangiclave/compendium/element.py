from typing import Any, Dict, Optional, List

from frangiclave.compendium.linked_recipe_details import \
    to_linked_recipe_details, LinkedRecipeDetails
from frangiclave.compendium.slot_specification import to_slot_specifications, \
    SlotSpecification
from frangiclave.compendium.utils import to_bool, to_int_dict, get


class Element:

    id: str
    label: Optional[str]
    description: Optional[str]
    anim_frames: int
    icon: Optional[str]
    lifetime: float
    decay_to: Optional[str]
    is_aspect: bool
    unique: bool
    aspects: Dict[str, int]
    induces: List[LinkedRecipeDetails]
    child_slots: List[SlotSpecification]
    x_triggers: Dict[str, str]
    no_art_needed: bool

    def __init__(
            self,
            _id: str,
            label: Optional[str] = None,
            description: Optional[str] = None,
            anim_frames: int = 0,
            icon: str = None,
            lifetime: float = 0.0,
            decay_to: str = None,
            is_aspect: bool = False,
            unique: bool = False,
            aspects: Dict[str, int] = None,
            induces: List[LinkedRecipeDetails] = None,
            slots: List[SlotSpecification] = None,
            x_triggers: Dict[str, str] = None,
            no_art_needed: bool = False
    ):
        self.id = _id
        self.label = label
        self.description = description
        self.anim_frames = anim_frames
        self.icon = icon
        self.lifetime = lifetime
        self.decay_to = decay_to
        self.is_aspect = is_aspect
        self.unique = unique
        self.aspects = aspects if aspects is not None else {}
        self.induces = induces if induces is not None else []
        self.child_slots = slots if slots is not None else []
        self.x_triggers = x_triggers if x_triggers is not None else {}
        self.no_art_needed = no_art_needed

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'Element':
        e = cls(data['id'])
        e.label = get(data, 'label')
        e.description = get(data, 'description')
        e.anim_frames = get(data, 'animFrames', 0, int)
        e.icon = get(data, 'icon', None)
        e.lifetime = get(data, 'lifetime', 0.0, float)
        e.decay_to = get(data, 'decayTo', None)
        e.is_aspect = get(data, 'isAspect', False, to_bool)
        e.unique = get(data, 'unique', False, to_bool)
        e.aspects = get(data, 'aspects', {}, to_int_dict)
        e.induces = get(data, 'induces', [], to_linked_recipe_details)
        e.child_slots = get(data, 'slots', [], to_slot_specifications)
        e.x_triggers = get(data, 'xtriggers', {})
        e.no_art_needed = get(data, 'noartneeded', False, to_bool)
        return e
