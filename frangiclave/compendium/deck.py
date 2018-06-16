from typing import Dict, List, Optional, Any

from sqlalchemy import Column, String, Boolean, PickleType, Integer, ForeignKey
from sqlalchemy.orm import relationship

from frangiclave.compendium.base import Base, GameContentMixin, Session
from frangiclave.compendium.file import File
from frangiclave.compendium.utils import to_bool, get


class Deck(Base, GameContentMixin):
    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True)
    deck_id = Column(String)
    file_id = Column(Integer, ForeignKey(File.id))

    starting_cards: List[str] = Column(PickleType)
    default_card_id = Column(String)
    reset_on_exhaustion = Column(Boolean)
    label = Column(String, nullable=True)
    description = Column(String, nullable=True)
    draw_messages: Dict[str, str] = Column(PickleType)
    default_draw_messages: Dict[str, str] = Column(PickleType)
    comment: Optional[str] = Column(String, nullable=True)

    file = relationship(File)

    def __init__(
            self,
            deck_id: str,
            file: str,
            spec: List[str] = None,
            default_card_id: Optional[str] = None,
            reset_on_exhaustion: bool = False,
            label: Optional[str] = None,
            description: Optional[str] = None,
            draw_messages: Optional[Dict[str, str]] = None,
            default_draw_messages: Optional[Dict[str, str]] = None,
            comment: str = None
    ):
        self.deck_id = deck_id
        self.file = file
        self.starting_cards = spec if spec is not None else []
        self.default_card_id = default_card_id
        self.reset_on_exhaustion = reset_on_exhaustion
        self.label = label
        self.description = description
        self.draw_messages = draw_messages if draw_messages is not None else {}
        self.default_draw_messages = default_draw_messages \
            if default_draw_messages is not None else {}
        self.comment = comment

    @classmethod
    def from_data(cls, file_name: str, data: Dict[str, Any]) -> 'Deck':
        d = cls(data['id'], file_name)
        d.starting_cards = get(data, 'spec', [])
        d.default_card_id = get(data, 'defaultcard', None)
        d.reset_on_exhaustion = get(
            data, 'resetonexhaustion', False, to_bool
        )
        d.label = get(data, 'label', None)
        d.description = get(data, 'description', None)
        d.draw_messages = get(data, 'drawmessages', {})
        d.default_draw_messages = get(data, 'defaultdrawmessages', {})
        d.comment = get(data, 'comment', None)
        return d

    @classmethod
    def get_by_deck_id(cls, session: Session, deck_id: str):
        return session.query(cls).filter(cls.deck_id == deck_id).one()
