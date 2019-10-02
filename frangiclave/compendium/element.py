from typing import TYPE_CHECKING, Any, Dict, Optional, List, Tuple

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from frangiclave.compendium.base import Base, Session
from frangiclave.compendium.file import File
from frangiclave.compendium.game_content import GameContentMixin, GameContents
from frangiclave.compendium.linked_recipe_details import LinkedRecipeDetails, \
    LinkedRecipeChallengeRequirement
from frangiclave.compendium.slot_specification import SlotSpecification
from frangiclave.compendium.utils import to_bool, get

if TYPE_CHECKING:
    from frangiclave.compendium.deck import Deck, DeckCard
    from frangiclave.compendium.recipe import RecipeRequirement, Recipe, \
    RecipeEffect


class ElementAspect(Base):
    __tablename__ = 'elements_aspects'

    id = Column(Integer, primary_key=True)

    element_id: int = Column(Integer, ForeignKey('elements.id'))
    element: 'Element' = relationship(
        'Element', back_populates='aspects', foreign_keys=element_id
    )
    aspect_id: int = Column(Integer, ForeignKey('elements.id'))
    aspect: 'Element' = relationship(
        'Element', back_populates='_aspect_for', foreign_keys=aspect_id
    )
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
    uniqueness_group: bool = Column(String, nullable=True)
    aspects: List[ElementAspect] = relationship(
        ElementAspect,
        back_populates='element',
        foreign_keys=ElementAspect.element_id
    )
    _aspect_for: List[ElementAspect] = relationship(
        ElementAspect,
        back_populates='aspect',
        foreign_keys=ElementAspect.aspect_id
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
    is_hidden: bool = Column(Boolean)
    no_art_needed: bool = Column(Boolean)
    resaturate: bool = Column(Boolean)
    verb_icon: str = Column(String)
    _in_decks: List['DeckCard'] = relationship(
        'DeckCard', back_populates='element'
    )
    in_decks_default: List['Deck'] = relationship(
        'Deck', back_populates='default_card'
    )
    _requirement_for_recipes: List['RecipeRequirement'] = relationship(
        'RecipeRequirement', back_populates='element'
    )
    _effect_of_recipes: List['RecipeEffect'] = relationship(
        'RecipeEffect', back_populates='element'
    )
    comments: Optional[str] = Column(String, nullable=True)

    @hybrid_property
    def aspect_for(self) -> Tuple['Element']:
        return tuple(sorted(
            set(ea.element for ea in self._aspect_for),
            key=lambda e: e.element_id
        ))

    @hybrid_property
    def in_decks(self) -> Tuple['Deck']:
        return tuple(sorted(
            list(dc.deck for dc in self._in_decks) + self.in_decks_default,
            key=lambda deck: deck.deck_id
        ))

    @hybrid_property
    def requirement_for_recipes(self) -> Tuple['Recipe']:
        return tuple(sorted(
            (rr.recipe for rr in self._requirement_for_recipes),
            key=lambda recipe: recipe.recipe_id
        ))

    @hybrid_property
    def effect_of_recipes(self) -> Tuple['Recipe']:
        return tuple(sorted(
            (rr.recipe for rr in self._effect_of_recipes),
            key=lambda recipe: recipe.recipe_id
        ))

    @classmethod
    def from_data(
            cls,
            file: File,
            data: Dict[str, Any],
            translations: Dict[str, Dict[str, Any]],
            game_contents: GameContents
    ) -> 'Element':
        e = game_contents.get_element(data['id'])
        e.file = file
        e.label = get(data, 'label', translations=translations)
        e.description = get(data, 'description', translations=translations)
        e.animation_frames = get(data, 'animFrames', 0, int)
        e.icon = get(data, 'icon')
        e.lifetime = get(data, 'lifetime', 0.0, float)
        e.decay_to = game_contents.get_element(get(data, 'decayTo', None))
        e.is_aspect = get(data, 'isAspect', False, to_bool)
        e.unique = get(data, 'unique', False, to_bool)
        e.uniqueness_group = get(data, 'uniquenessgroup')
        e.aspects = [
            ElementAspect(
                element=e,
                aspect=game_contents.get_element(aspect_id),
                quantity=int(quantity)
            ) for aspect_id, quantity in get(data, 'aspects', {}).items()
        ]
        e.induces = [
            ElementLinkedRecipeDetails.from_data(
                v,
                ElementLinkedRecipeDetailsChallengeRequirement,
                game_contents
            )
            for v in get(data, 'induces', [])
        ]
        e.child_slots = [
            ElementSlotSpecification.from_data(v, {
                c: c_transformation["slots"][i]
                for c, c_transformation in translations.items()
                if "slots" in c_transformation
            }, game_contents)
            for i, v in enumerate(get(data, 'slots', []))
        ]
        e.x_triggers = [
            ElementXTrigger(
                trigger=game_contents.get_element(trigger_id),
                result=game_contents.get_element(result_id)
            ) for trigger_id, result_id in get(data, 'xtriggers', {}).items()
        ]
        e.is_hidden = get(data, 'isHidden', False, to_bool)
        e.no_art_needed = get(data, 'noartneeded', False, to_bool)
        e.resaturate = get(data, 'resaturate', False, to_bool)
        e.verb_icon = get(data, 'verbicon')
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
    challenges = relationship('ElementLinkedRecipeDetailsChallengeRequirement')


class ElementLinkedRecipeDetailsChallengeRequirement(
    Base, LinkedRecipeChallengeRequirement
):
    __tablename__ = 'elements_linked_recipe_details_challenge_requirement'

    id = Column(Integer, primary_key=True)

    linked_recipe_details_id: int = Column(
        Integer, ForeignKey(ElementLinkedRecipeDetails.id))
    linked_recipe_details: ElementLinkedRecipeDetails = \
        relationship(
            ElementLinkedRecipeDetails,
            back_populates='challenges',
            foreign_keys=linked_recipe_details_id
        )


class ElementSlotSpecification(Base, SlotSpecification):
    __tablename__ = 'elements_slot_specifications'

    id = Column(Integer, primary_key=True)

    element_id: int = Column(Integer, ForeignKey(Element.id))
    element: Element = relationship(Element, back_populates='child_slots')
