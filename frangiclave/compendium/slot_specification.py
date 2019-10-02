from typing import TYPE_CHECKING, Any, Dict, List

from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Table
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from frangiclave.compendium.base import Base
from frangiclave.compendium.game_content import GameContents
from frangiclave.compendium.utils import get, to_bool

if TYPE_CHECKING:
    from frangiclave.compendium.verb import Verb


class SlotSpecification:
    __tablename__ = None

    label: str = Column(String)
    description: str = Column(String)

    @declared_attr
    def required(self) -> List['SlotSpecificationItem']:
        return relationship(
            'SlotSpecificationItem',
            secondary=lambda: self.secondary('required')
        )

    @declared_attr
    def forbidden(self) -> List['SlotSpecificationItem']:
        return relationship(
            'SlotSpecificationItem',
            secondary=lambda: self.secondary('forbidden')
        )

    @classmethod
    def secondary(cls, attr: str):
        return Table(
            cls.__tablename__ + '_' + attr + '_items_associations',
            Base.metadata,
            Column(
                'slot_specification_id',
                Integer,
                ForeignKey(cls.__tablename__ + '.id')
            ),
            Column(
                'item_id',
                Integer,
                ForeignKey('slot_specification_items.id')
            )
        )

    greedy: bool = Column(Boolean)
    consumes: bool = Column(Boolean)
    no_animation: bool = Column(Boolean)

    @declared_attr
    def for_verb_id(self) -> Column:
        return Column(Integer, ForeignKey('verbs.id'))

    @declared_attr
    def for_verb(self) -> 'Verb':
        return relationship('Verb', foreign_keys=self.for_verb_id)

    @classmethod
    def from_data(
            cls,
            data: Dict[str, Any],
            translations: Dict[str, Dict[str, Any]],
            game_contents: GameContents
    ) -> 'SlotSpecification':
        s = cls()
        s.element = game_contents.get_element(data['id'])
        s.label = get(
            data, 'label', s.element.element_id, translations=translations
        )
        s.description = get(data, 'description', '', translations=translations)
        s.required = [
            SlotSpecificationItem(
                element=game_contents.get_element(element_id),
                quantity=quantity
            ) for element_id, quantity in get(data, 'required', {}).items()
        ]
        s.forbidden = [
            SlotSpecificationItem(
                element=game_contents.get_element(element_id),
                quantity=quantity
            ) for element_id, quantity in get(data, 'forbidden', {}).items()
        ]
        s.greedy = get(data, 'greedy', False, to_bool)
        s.consumes = get(data, 'consumes', False, to_bool)
        s.no_animation = get(data, 'noanim', False, to_bool)
        s.for_verb = game_contents.get_verb(get(data, 'actionId', None))
        return s


class SlotSpecificationItem(Base):
    __tablename__ = 'slot_specification_items'

    id = Column(Integer, primary_key=True)
    element_id = Column(Integer, ForeignKey('elements.id'))
    element = relationship('Element')
    quantity = Column(Integer)
