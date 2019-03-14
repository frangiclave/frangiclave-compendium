from typing import TYPE_CHECKING, Dict, List, Optional, Any, Tuple

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from frangiclave.compendium.base import Base, Session
from frangiclave.compendium.file import File
from frangiclave.compendium.game_content import GameContentMixin, GameContents
from frangiclave.compendium.utils import to_bool, get

if TYPE_CHECKING:
    from frangiclave.compendium.element import Element


class DeckCard(Base):
    __tablename__ = 'deck_cards'

    id = Column(Integer, primary_key=True)
    deck_id: int = Column(Integer, ForeignKey('decks.id'))
    deck: 'Deck' = relationship(
        'Deck', back_populates='_cards', foreign_keys=deck_id
    )
    element_id: int = Column(Integer, ForeignKey('elements.id'))
    element: 'Element' = relationship(
        'Element', back_populates='_in_decks', foreign_keys=element_id
    )


class Deck(Base, GameContentMixin):
    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True)
    deck_id: str = Column(String, unique=True)

    _cards: List[DeckCard] = relationship(
        'DeckCard',
        back_populates='deck',
    )

    default_card_id = Column(Integer, ForeignKey('elements.id'))
    default_card = relationship('Element', back_populates='in_decks_default')
    reset_on_exhaustion = Column(Boolean)
    label = Column(String, nullable=True)
    description = Column(String, nullable=True)
    all_draw_messages: List['DeckDrawMessage'] = relationship(
        'DeckDrawMessage', back_populates='deck'
    )
    comments: Optional[str] = Column(String, nullable=True)

    @hybrid_property
    def cards(self) -> Tuple['Element']:
        return tuple(sorted(
            (dc.element for dc in self._cards),
            key=lambda e: e.element_id
        ))

    @hybrid_property
    def draw_messages(self) -> Tuple['DeckDrawMessage']:
        return tuple(dm for dm in self.all_draw_messages if not dm.default)

    @hybrid_property
    def default_draw_messages(self) -> Tuple['DeckDrawMessage']:
        return tuple(dm for dm in self.all_draw_messages if dm.default)

    @classmethod
    def from_data(
            cls,
            file: File,
            data: Dict[str, Any],
            game_contents: GameContents
    ) -> 'Deck':
        d = game_contents.get_deck(data['id'])
        d.file = file
        d._cards = [
            DeckCard(element=game_contents.get_element(c))
            for c in get(data, 'spec', [])
        ]
        d.default_card = game_contents.get_element(
            get(data, 'defaultcard', None)
        )
        d.reset_on_exhaustion = get(data, 'resetonexhaustion', False, to_bool)
        d.label = get(data, 'label', None)
        d.description = get(data, 'description', None)
        d.all_draw_messages = [
            DeckDrawMessage(
                element=game_contents.get_element(element_id),
                message=message
            ) for element_id, message in get(data, 'drawmessages', {}).items()
        ] + [
            DeckDrawMessage(
                element=game_contents.get_element(element_id),
                message=message,
                default=True
            ) for element_id, message in get(
                data, 'defaultdrawmessages', {}
            ).items()
        ]
        d.comments = get(data, 'comments', None)
        return d

    @classmethod
    def get_by_deck_id(cls, session: Session, deck_id: str) -> 'Deck':
        return session.query(cls).filter(cls.deck_id == deck_id).one()


class DeckDrawMessage(Base):
    __tablename__ = 'decks_draw_messages'

    id = Column(Integer, primary_key=True)
    deck_id = Column(Integer, ForeignKey(Deck.id))
    deck = relationship('Deck', back_populates='all_draw_messages')
    element_id = Column(Integer, ForeignKey('elements.id'))
    element = relationship('Element')
    message = Column(String)
    default = Column(Boolean, default=False)
