from typing import Optional, Dict, Any

from sqlalchemy import Column, Enum as EnumType, String, Integer

from frangiclave.compendium.base import Base, Session
from frangiclave.compendium.ending_flavour import EndingFlavour
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
            data: Dict[str, Any]
    ) -> 'Ending':
        e = Ending()
        e.ending_id = get(data, 'id')
        e.title = get(data, 'title')
        e.description = get(data, 'description')
        e.image = get(data, 'imageId')
        e.flavour = EndingFlavour(get(data, 'endingFlavour', 'None'))
        e.animation = get(data, 'anim')
        e.achievement = get(data, 'achievementId')
        return e

    @classmethod
    def get_by_ending_id(cls, session: Session, ending_id: str) -> 'Ending':
        return session.query(cls).filter(cls.ending_id == ending_id).one()
