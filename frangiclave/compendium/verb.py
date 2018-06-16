from typing import Any, Dict, Optional

from frangiclave.compendium.slot_specification import SlotSpecification, \
    to_slot_specifications
from frangiclave.compendium.utils import to_bool, get


class Verb:

    id: str
    label: Optional[str]
    description: Optional[str]
    at_start: bool
    primary_slot_specification: Optional[SlotSpecification]

    def __init__(
            self,
            _id: str,
            label: Optional[str] = None,
            description: Optional[str] = None,
            at_start: bool = False,
            primary_slot_specification: Optional[SlotSpecification] = None
    ):
        self.id = _id
        self.label = label
        self.description = description
        self.at_start = at_start
        self.primary_slot_specification = primary_slot_specification

    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        r = cls(data['id'])
        r.label = get(data, 'label')
        r.description = get(data, 'description')
        r.at_start = get(data, 'atStart', False, to_bool)
        if 'slots' in data:
            slots = to_slot_specifications(data['slots'])
            if slots:
                r.primary_slot_specification = slots[0]
        return r
