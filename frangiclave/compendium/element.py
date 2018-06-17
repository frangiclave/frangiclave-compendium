from typing import TYPE_CHECKING, Any, Dict, Optional, List

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from frangiclave.compendium.base import Base, Session
from frangiclave.compendium.file import File
from frangiclave.compendium.game_content import GameContentMixin, GameContents
from frangiclave.compendium.linked_recipe_details import LinkedRecipeDetails
from frangiclave.compendium.slot_specification import SlotSpecification
from frangiclave.compendium.utils import to_bool, get

if TYPE_CHECKING:
    from frangiclave.compendium.deck import Deck


class ElementAspect(Base):
    __tablename__ = 'elements_aspects'

    id = Column(Integer, primary_key=True)

    element_id: int = Column(Integer, ForeignKey('elements.id'))
    element: 'Element' = relationship(
        'Element', back_populates='aspects', foreign_keys=element_id
    )
    aspect_id: int = Column(Integer, ForeignKey('elements.id'))
    aspect: 'Element' = relationship('Element', foreign_keys=aspect_id)
    quantity: int = Column(Integer)


class ElementXTrigger(Base):
    __tablename__ = 'elements_x_triggers'

    id = Column(Integer, primary_key=True)

    element_id: int = Column(Integer, ForeignKey('elements.id'))
    element: 'Element' = relationship(
        'Element', back_populates='x_triggers', foreign_keys=element_id
    )
    trigger_id: int = Column(Integer, ForeignKey('elements.id'))
    trigger: 'Element' = relationship(
        'Element', back_populates='triggered_with', foreign_keys=trigger_id
    )
    result_id: int = Column(Integer, ForeignKey('elements.id'))
    result: 'Element' = relationship(
        'Element', back_populates='triggered_by', foreign_keys=result_id
    )


class Element(Base, GameContentMixin):
    __tablename__ = 'elements'

    id = Column(Integer, primary_key=True)
    element_id: str = Column(String, unique=True)

    label: Optional[str] = Column(String, nullable=True)
    description: Optional[str] = Column(String, nullable=True)
    animation_frames: int = Column(Integer, default=0)
    icon: Optional[str] = Column(String, nullable=True)
    lifetime: Optional[float] = Column(Float, nullable=True)
    decay_to_id: Optional[int] = Column(Integer, ForeignKey('elements.id'))
    decay_to = relationship(
        'Element',
        back_populates='decay_from',
        remote_side=id
    )
    decay_from = relationship(
        'Element',
        back_populates='decay_to'
    )
    is_aspect: bool = Column(Boolean)
    unique: bool = Column(Boolean)
    aspects: List[ElementAspect] = relationship(
        ElementAspect,
        back_populates='element',
        foreign_keys=ElementAspect.element_id
    )
    induces: List['ElementLinkedRecipeDetails'] = relationship(
        'ElementLinkedRecipeDetails', back_populates='element'
    )
    child_slots: List['ElementSlotSpecification'] = relationship(
        'ElementSlotSpecification', back_populates='element'
    )
    x_triggers: List[ElementXTrigger] = relationship(
        ElementXTrigger,
        back_populates='element',
        foreign_keys=ElementXTrigger.element_id
    )
    triggered_with: List[ElementXTrigger] = relationship(
        ElementXTrigger,
        back_populates='trigger',
        foreign_keys=ElementXTrigger.trigger_id
    )
    triggered_by: List[ElementXTrigger] = relationship(
        ElementXTrigger,
        back_populates='result',
        foreign_keys=ElementXTrigger.result_id
    )
    no_art_needed: bool = Column(Boolean)
    in_decks: List['Deck'] = relationship(
        'Deck', secondary='decks_cards', back_populates='cards'
    )
    in_decks_default: List['Deck'] = relationship(
        'Deck', back_populates='default_card'
    )
    comments: Optional[str] = Column(String, nullable=True)

    @classmethod
    def from_data(
            cls,
            file: File,
            data: Dict[str, Any],
            game_contents: GameContents
    ) -> 'Element':
        e = game_contents.get_element(data['id'])
        e.file = file
        e.label = get(data, 'label')
        e.description = get(data, 'description')
        e.animation_frames = get(data, 'animFrames', 0, int)
        e.icon = get(data, 'icon', None)
        e.lifetime = get(data, 'lifetime', 0.0, float)
        e.decay_to = game_contents.get_element(get(data, 'decayTo', None))
        e.is_aspect = get(data, 'isAspect', False, to_bool)
        e.unique = get(data, 'unique', False, to_bool)
        e.aspects = [
            ElementAspect(
                element=e,
                aspect=game_contents.get_element(aspect_id),
                quantity=int(quantity)
            ) for aspect_id, quantity in get(data, 'aspects', {}).items()
        ]
        e.induces = [
            ElementLinkedRecipeDetails.from_data(v, game_contents)
            for v in get(data, 'induces', [])
        ]
        e.child_slots = [
            ElementSlotSpecification.from_data(v, game_contents)
            for v in get(data, 'slots', [])
        ]
        e.x_triggers = [
            ElementXTrigger(
                trigger=game_contents.get_element(trigger_id),
                result=game_contents.get_element(result_id)
            ) for trigger_id, result_id in get(data, 'xtriggers', {}).items()
        ]
        e.no_art_needed = get(data, 'noartneeded', False, to_bool)
        e.comments = get(data, 'comments', None)
        return e

    @classmethod
    def get_by_element_id(cls, session: Session, element_id: str) -> 'Element':
        return session.query(cls).filter(cls.element_id == element_id).one()


class ElementLinkedRecipeDetails(Base, LinkedRecipeDetails):
    __tablename__ = 'elements_linked_recipe_details'

    id = Column(Integer, primary_key=True)

    element_id: int = Column(Integer, ForeignKey(Element.id))
    element: Element = relationship(Element, back_populates='induces')


class ElementSlotSpecification(Base, SlotSpecification):
    __tablename__ = 'elements_slot_specifications'

    id = Column(Integer, primary_key=True)

    element_id: int = Column(Integer, ForeignKey(Element.id))
    element: Element = relationship(Element, back_populates='child_slots')
