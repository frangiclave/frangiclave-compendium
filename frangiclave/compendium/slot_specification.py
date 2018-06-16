from typing import Any, Dict, List

from frangiclave.compendium.utils import get, to_bool


class SlotSpecification:

    id: str
    label: str
    description: str
    required: Dict[str, int]
    forbidden: Dict[str, int]
    greedy: bool
    consumes: bool
    no_animation: bool
    for_verb: str

    def __init__(
            self,
            _id: str,
            label: str = '',
            description: str = '',
            required: Dict[str, int] = None,
            forbidden: Dict[str, int] = None,
            greedy: bool = False,
            consumes: bool = False,
            no_animation: bool = False,
            for_verb: str = None
    ):
        self.id = _id
        self.label = label
        self.description = description
        self.required = required if required is not None else {}
        self.forbidden = forbidden if forbidden is not None else {}
        self.greedy = greedy
        self.consumes = consumes
        self.no_animation = no_animation
        self.for_verb = for_verb

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'SlotSpecification':
        s = cls(data['id'])
        s.label = get(data, 'label', s.id)
        s.description = get(data, 'description', '')
        s.required = get(data, 'required', {})
        s.forbidden = get(data, 'forbidden', {})
        s.greedy = get(data, 'greedy', False, to_bool)
        s.consumes = get(data, 'consumes', False, to_bool)
        s.no_animation = get(data, 'noanim', False, to_bool)
        s.for_verb = get(data, 'actionId', None)
        return s


def to_slot_specifications(
        val: List[Dict[str, Any]]
) -> List['SlotSpecification']:
    return [SlotSpecification.from_data(v) for v in val]
