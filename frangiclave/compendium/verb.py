from typing import Any, Dict, Optional

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from frangiclave.compendium.base import Base, Session
from frangiclave.compendium.file import File
from frangiclave.compendium.game_content import GameContentMixin, GameContents
from frangiclave.compendium.slot_specification import SlotSpecification
from frangiclave.compendium.utils import to_bool, get


class Verb(Base, GameContentMixin):
    __tablename__ = 'verbs'

    id = Column(Integer, primary_key=True)
    verb_id: str = Column(String, unique=True)

    label: Optional[str] = Column(String, nullable=True)
    description: Optional[str] = Column(String, nullable=True)
    at_start: bool = Column(Boolean)
    primary_slot_specification_id: int = Column(
        Integer, ForeignKey('verbs_slot_specifications.id')
    )
    primary_slot_specification: Optional['VerbSlotSpecification'] = \
        relationship(
            'VerbSlotSpecification',
            foreign_keys=primary_slot_specification_id
    )
    recipes = relationship('Recipe', back_populates='action')
    comments: Optional[str] = Column(String, nullable=True)

    @classmethod
    def from_data(
            cls,
            file: File,
            data: Dict[str, Any],
            game_contents: GameContents
    ):
        r = game_contents.get_verb(data['id'])
        r.file = file
        r.label = get(data, 'label')
        r.description = get(data, 'description')
        r.at_start = get(data, 'atStart', False, to_bool)
        if 'slots' in data and data['slots']:
            r.primary_slot_specification = VerbSlotSpecification.from_data(
                data['slots'][0], game_contents
            )
        r.comments = get(data, 'comments', None)
        return r

    @classmethod
    def get_by_verb_id(cls, session: Session, verb_id: str) -> 'Verb':
        return session.query(cls).filter(cls.verb_id == verb_id).one()


class VerbSlotSpecification(Base, SlotSpecification):
    __tablename__ = 'verbs_slot_specifications'

    id = Column(Integer, primary_key=True)
