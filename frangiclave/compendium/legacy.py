from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Session, relationship

from frangiclave.compendium.base import Base
from frangiclave.compendium.file import File
from frangiclave.compendium.game_content import GameContents, GameContentMixin
from frangiclave.compendium.utils import to_bool, get

if TYPE_CHECKING:
    from frangiclave.compendium.element import Element


class Legacy(Base, GameContentMixin):
    __tablename__ = 'legacies'

    id = Column(Integer, primary_key=True)
    legacy_id: str = Column(String, unique=True)

    label: str = Column(String)
    description: str = Column(String)
    start_description: str = Column(String)
    image: str = Column(String)
    from_ending: str = Column(String)
    available_without_ending_match: bool = Column(Boolean)
    effects: List['LegacyEffect'] = relationship('LegacyEffect')
    comments: Optional[str] = Column(String, nullable=True)

    @classmethod
    def from_data(
            cls,
            file: File,
            data: Dict[str, Any],
            game_contents: GameContents
    ) -> 'Legacy':
        lg = game_contents.get_legacy(data['id'])
        lg.file = file
        lg.label = get(data, 'label')
        lg.description = get(data, 'description')
        lg.start_description = get(data, 'startdescription')
        lg.image = get(data, 'image')
        lg.from_ending = get(data, 'fromEnding')
        lg.available_without_ending_match = get(
            data, 'availableWithoutEndingMatch', False, to_bool
        )
        lg.effects = LegacyEffect.from_data(
            get(data, 'effects', {}), game_contents
        )
        return lg

    @classmethod
    def get_by_legacy_id(cls, session: Session, legacy_id: str) -> 'Legacy':
        return session.query(cls).filter(cls.legacy_id == legacy_id).one()


class LegacyEffect(Base):
    __tablename__ = 'legacies_effects'

    id = Column(Integer, primary_key=True)
    legacy_id = Column(Integer, ForeignKey(Legacy.id))

    element_id: int = Column(Integer, ForeignKey('elements.id'))
    element: 'Element' = relationship('Element')

    quantity = Column(Integer)

    @classmethod
    def from_data(cls, val: Dict[str, str], game_contents: GameContents):
        return [
            cls(
                element=game_contents.get_element(element_id),
                quantity=int(quantity)
            )
            for element_id, quantity in val.items()
        ]
