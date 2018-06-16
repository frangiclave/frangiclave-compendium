from typing import Any, Dict, Optional

from frangiclave.compendium.utils import to_bool, to_int_dict, get


class Legacy:

    id: str
    label: str
    description: str
    start_description: str
    image: str
    from_ending: Optional[str]
    available_without_ending_match: bool
    effects: Dict[str, int]

    def __init__(
            self,
            _id: str,
            label: str = '',
            description: str = '',
            start_description: str = '',
            image: str = '',
            from_ending: str = None,
            available_without_ending_match: bool = False,
            effects: Dict[str, int] = None
    ):
        self.id = _id
        self.label = label
        self.description = description
        self.start_description = start_description
        self.image = image
        self.from_ending = from_ending
        self.available_without_ending_match = available_without_ending_match
        self.effects = effects if effects is not None else {}

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'Legacy':
        lg = cls(data['id'])
        lg.label = get(data, 'label', '')
        lg.description = get(data, 'description', '')
        lg.start_description = get(data, 'startdescription', '')
        lg.image = get(data, 'image', '')
        lg.from_ending = get(data, 'fromEnding', None)
        lg.available_without_ending_match = get(
            data, 'availableWithoutEndingMatch', False, to_bool
        )
        lg.effects = get(data, 'effects', {}, to_int_dict)
        return lg
