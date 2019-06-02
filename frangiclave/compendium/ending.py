from typing import Optional, Dict, Any

from sqlalchemy import Column, Enum as EnumType, String, Integer

from frangiclave.compendium.base import Base, Session
from frangiclave.compendium.ending_flavour import EndingFlavour
from frangiclave.compendium.file import File
from frangiclave.compendium.game_content import GameContents
from frangiclave.compendium.utils import get


class Ending(Base):
    __tablename__ = 'endings'

    id = Column(Integer, primary_key=True)

    ending_id: int = Column(String, unique=True)
    title: Optional[str] = Column(String, nullable=True)
    description: str = Column(String)
    image: str = Column(String)
    flavour: EndingFlavour = Column(EnumType(EndingFlavour, name='flavour'))
    animation: str = Column(String)
    achievement: Optional[str] = Column(String, nullable=True)

    @classmethod
    def from_data(
            cls,
            file: File,
            data: Dict[str, Any],
            game_contents: GameContents
    ) -> 'Ending':
        e = game_contents.get_ending(get(data, 'id'))
        e.file = file
        e.title = get(data, 'label')
        e.description = get(data, 'description')
        e.image = get(data, 'image')
        e.flavour = EndingFlavour(get(data, 'flavour', 'None'))
        e.animation = get(data, 'anim')
        e.achievement = get(data, 'achievement')
        return e

    @classmethod
    def get_by_ending_id(cls, session: Session, ending_id: str) -> 'Ending':
        return session.query(cls).filter(cls.ending_id == ending_id).one()
