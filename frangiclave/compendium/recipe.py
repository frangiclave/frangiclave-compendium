import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, \
    Enum as EnumType
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from frangiclave.compendium.base import Base, Session
from frangiclave.compendium.file import File
from frangiclave.compendium.game_content import GameContentMixin, GameContents
from frangiclave.compendium.linked_recipe_details import LinkedRecipeDetails
from frangiclave.compendium.slot_specification import SlotSpecification
from frangiclave.compendium.utils import to_bool, get


if TYPE_CHECKING:
    from frangiclave.compendium.element import Element
    from frangiclave.compendium.deck import Deck


class EndingFlavour(Enum):
    NONE = 'none'
    GRAND = 'grand'
    MELANCHOLY = 'melancholy'


class PortalEffect(Enum):
    NONE = 'none'
    WOOD = 'wood'
    WHITEDOOR = 'whitedoor'
    STAGDOOR = 'stagdoor'
    SPIDERDOOR = 'spiderdoor'
    PEACOCKDOOR = 'peacockdoor'
    TRICUSPIDGATE = 'tricuspidgate'


class MutationEffect(Base):
    __tablename__ = 'mutation_effects'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    recipe = relationship('Recipe', back_populates='mutation_effects')
    filter_on_aspect_id = Column(Integer, ForeignKey('elements.id'))
    filter_on_aspect = relationship(
        'Element', foreign_keys=filter_on_aspect_id
    )
    mutate_aspect_id = Column(Integer, ForeignKey('elements.id'))
    mutate_aspect = relationship('Element', foreign_keys=mutate_aspect_id)
    mutation_level = Column(Integer)
    additive = Column(Boolean)

    @classmethod
    def from_data(cls, val: List[Dict[str, str]], game_contents: GameContents):
        return [
            MutationEffect(
                filter_on_aspect=game_contents.get_element(
                    v['filterOnAspectId']
                ),
                mutate_aspect=game_contents.get_element(v['mutateAspectId']),
                mutation_level=int(v['mutationLevel']),
                additive=get(v, 'additive', False, to_bool)
            )
            for v in val
        ]


class Recipe(Base, GameContentMixin):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    recipe_id: str = Column(String, unique=True)

    label: str = Column(String)
    start_description: Optional[str] = Column(String, nullable=True)
    description: Optional[str] = Column(String, nullable=True)
    action_id: Optional[int] = Column(
        Integer,
        ForeignKey('verbs.id'),
        nullable=True
    )
    action = relationship(
        'Verb',
        foreign_keys=action_id,
        back_populates='recipes'
    )
    requirements: List['RecipeRequirement'] = relationship('RecipeRequirement')
    effects: List['RecipeEffect'] = relationship('RecipeEffect')
    aspects: List['RecipeAspect'] = relationship('RecipeAspect')
    mutation_effects: List[MutationEffect] = relationship(
        MutationEffect, back_populates='recipe'
    )
    signal_ending_flavour: EndingFlavour = Column(
        EnumType(EndingFlavour, name='ending_flavour')
    )
    craftable: bool = Column(Boolean)
    hint_only: bool = Column(Boolean)
    warmup: int = Column(Integer)
    deck_effect: List['RecipeDeckEffect'] = relationship('RecipeDeckEffect')
    alternative_recipes: List['RecipeAlternativeRecipeDetails'] = relationship(
        'RecipeAlternativeRecipeDetails',
        back_populates='source_recipe',
        foreign_keys='RecipeAlternativeRecipeDetails.source_recipe_id'
    )
    linked_recipes: List['RecipeLinkedRecipeDetails'] = relationship(
        'RecipeLinkedRecipeDetails',
        back_populates='source_recipe',
        foreign_keys='RecipeLinkedRecipeDetails.source_recipe_id'
    )
    ending_flag: Optional[str] = Column(String, nullable=True)
    max_executions: int = Column(Integer)
    burn_image: Optional[str] = Column(String, nullable=True)
    portal_effect: PortalEffect = Column(
        EnumType(PortalEffect, name='portal_effect')
    )
    slot_specifications: List['RecipeSlotSpecification'] = relationship(
        'RecipeSlotSpecification', back_populates='recipe'
    )
    signal_important_loop: bool = Column(Boolean)
    comments: Optional[str] = Column(String, nullable=True)

    @classmethod
    def from_data(
            cls,
            file: File,
            data: Dict[str, Any],
            game_contents: GameContents
    ) -> 'Recipe':
        r = game_contents.get_recipe(data['id'])
        r.file = file
        r.label = get(data, 'label', data['id'])
        r.start_description = get(data, 'startdescription')
        r.description = get(data, 'description')
        r.action = game_contents.get_verb(get(data, 'actionId'))
        r.requirements = RecipeRequirement.from_data(
            get(data, 'requirements', {}), game_contents
        )
        r.effects = RecipeEffect.from_data(
            get(data, 'effects', {}), game_contents
        )
        if 'aspects' in data:
            # TODO Remove this when fixed
            if isinstance(data['aspects'], str):
                logging.error('Invalid value for aspects for recipe {}'.format(
                    data['id']
                ))
            else:
                r.aspects = RecipeAspect.from_data(
                    get(data, 'aspects', {}), game_contents
                )
        r.mutation_effects = MutationEffect.from_data(
            get(data, 'mutations', []), game_contents
        )
        r.signal_ending_flavour = EndingFlavour(get(
            data, 'signalEndingFlavour', 'none'
        ).lower())
        r.craftable = get(data, 'craftable', False, to_bool)
        r.hint_only = get(data, 'hintonly', False, to_bool)
        r.warmup = get(data, 'warmup', 0, int)
        r.deck_effect = RecipeDeckEffect.from_data(
            get(data, 'deckeffect', {}), game_contents
        )
        r.alternative_recipes = [
            RecipeAlternativeRecipeDetails.from_data(lrd, game_contents)
            for lrd in get(data, 'alternativerecipes', [])
        ]
        r.linked_recipes = [
            RecipeLinkedRecipeDetails.from_data(lrd, game_contents)
            for lrd in get(data, 'linked', [])
        ]
        r.ending_flag = get(data, 'ending')
        r.max_executions = get(data, 'maxexecutions', 0, int)
        r.burn_image = get(data, 'burnimage')
        r.portal_effect = PortalEffect(
            get(data, 'portaleffect', 'none').lower()
        )
        r.slot_specifications = [
            RecipeSlotSpecification.from_data(v, game_contents)
            for v in get(data, 'slots', [])]
        r.signal_important_loop = get(
            data, 'signalimportantloop', False, to_bool
        )
        return r

    @classmethod
    def get_by_recipe_id(cls, session: Session, recipe_id: str) -> 'Recipe':
        return session.query(cls).filter(cls.recipe_id == recipe_id).one()


class ElementQuantity:

    id = Column(Integer, primary_key=True)

    @declared_attr
    def recipe_id(self) -> Column:
        return Column(Integer, ForeignKey(Recipe.id))

    @declared_attr
    def element_id(self) -> Column:
        return Column(Integer, ForeignKey('elements.id'))

    @declared_attr
    def element(self) -> 'Element':
        return relationship('Element')

    quantity = Column(Integer)

    @classmethod
    def from_data(cls, val: Dict[str, str], game_contents: GameContents):
        return [
            ElementQuantity(
                element=game_contents.get_element(element_id),
                quantity=int(quantity)
            )
            for element_id, quantity in val.items()
        ]


class DeckQuantity:

    id = Column(Integer, primary_key=True)

    @declared_attr
    def recipe_id(self) -> Column:
        return Column(Integer, ForeignKey(Recipe.id))

    @declared_attr
    def deck_id(self) -> Column:
        return Column(Integer, ForeignKey('decks.id'))

    @declared_attr
    def deck(self) -> 'Deck':
        return relationship('Deck')

    quantity = Column(Integer)

    @classmethod
    def from_data(cls, val: Dict[str, str], game_contents: GameContents):
        return [
            DeckQuantity(
                deck=game_contents.get_deck(deck_id),
                quantity=int(quantity)
            )
            for deck_id, quantity in val.items()
        ]


class RecipeRequirement(Base, ElementQuantity):
    __tablename__ = 'recipes_requirements'


class RecipeEffect(Base, ElementQuantity):
    __tablename__ = 'recipes_effects'


class RecipeAspect(Base, ElementQuantity):
    __tablename__ = 'recipes_aspects'


class RecipeDeckEffect(Base, DeckQuantity):
    __tablename__ = 'recipes_deck_effects'


class RecipeAlternativeRecipeDetails(Base, LinkedRecipeDetails):
    __tablename__ = 'recipes_alternative_recipe_details'

    id = Column(Integer, primary_key=True)

    source_recipe_id: int = Column(Integer, ForeignKey(Recipe.id))
    source_recipe: Recipe = relationship(
        Recipe,
        back_populates='alternative_recipes',
        foreign_keys=source_recipe_id
    )


class RecipeLinkedRecipeDetails(Base, LinkedRecipeDetails):
    __tablename__ = 'recipes_linked_recipe_details'

    id = Column(Integer, primary_key=True)

    source_recipe_id: int = Column(Integer, ForeignKey(Recipe.id))
    source_recipe: Recipe = relationship(
        Recipe,
        back_populates='linked_recipes',
        foreign_keys=source_recipe_id
    )


class RecipeSlotSpecification(Base, SlotSpecification):
    __tablename__ = 'recipes_slot_specifications'

    id = Column(Integer, primary_key=True)

    recipe_id: int = Column(Integer, ForeignKey(Recipe.id))
    recipe: Recipe = relationship(Recipe, back_populates='slot_specifications')
