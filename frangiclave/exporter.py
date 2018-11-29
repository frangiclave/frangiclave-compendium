from typing import List, Tuple, Union, Dict, Any, Optional

from collections import OrderedDict, defaultdict

import json

from sqlalchemy.orm import Session

from frangiclave.compendium.base import get_session
from frangiclave.compendium.deck import Deck, DeckDrawMessage
from frangiclave.compendium.element import Element
from frangiclave.compendium.legacy import Legacy
from frangiclave.compendium.recipe import Recipe
from frangiclave.compendium.verb import Verb
from frangiclave.compendium.file import File
from frangiclave.compendium.slot_specification import SlotSpecification

def export_compendium(session: Session) -> Any:
    file_list = session.query(File).order_by(File.name).all()
    files = defaultdict(lambda: OrderedDict())
    decks = (
        session.query(Deck)
        .order_by(Deck.deck_id)
        .all()
    )
    elements = (
        session.query(Element)
        .order_by(Element.element_id)
        .all()
    )
    legacies = (
        session.query(Legacy)
        .order_by(Legacy.legacy_id)
        .all()
    )
    recipes = (
        session.query(Recipe)
        .order_by(Recipe.recipe_id)
        .all()
    )
    verbs = (
        session.query(Verb)
        .order_by(Verb.verb_id)
        .all()
    )
    items = decks + elements + legacies + recipes + verbs
    for file in file_list:
        files[file.category.value][file] = [
            item for item in items if item.file_id == file.id
        ]
    for category in files:
        for file in files[category]:
            print("exporting " + category + " " + file.name)
            content = {}
            objs = []
            for item in files[category][file]:
                objs += [dict_one_item(item, category)]
            content[category] = objs
            
            output_string = json.dumps(content, indent=4)
            game_dir_base = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Cultist Simulator\\"
            game_dir_cont = "cultistsimulator_Data\\StreamingAssets\\content\\"
            f = open(game_dir_base + game_dir_cont + file.group.value + "\\" + file.category.value + "\\" + file.name, "w")
            f.write(output_string)
            f.close()

def dict_one_item(item, category):
    if category == "recipes":
        return dict_one_recipe(item)
    elif category == "verbs":
        return dict_one_verb(item)
    elif category == "decks":
        return dict_one_deck(item)
    elif category == "legacies":
        return dict_one_legacy(item)
    elif category == "elements":
        return dict_one_element(item)
    else:
        print("Wrong category")
        return None
    
def dict_one_element(elem):
    content = {}
    content["id"] = elem.element_id
    if (elem.label):
        content["label"] = elem.label
    if (elem.description):
        content["description"] = elem.description
    if (elem.aspects):
        aspects = {}
        for aspect in elem.aspects:
            aspects[aspect.aspect.element_id] = aspect.quantity
        content["aspects"] = aspects
    if (elem.animation_frames != 0):
        content["animFrames"] = elem.animation_frames
    if (elem.icon):
        content["icon"] = elem.icon
    if (elem.lifetime != 0):
        content["lifetime"] = elem.lifetime
    if (elem.unique):
        content["unique"] = elem.unique
    if (elem.decay_to):
        content["decayTo"] = elem.decay_to.element_id
    if (elem.is_aspect):
        content["isAspect"] = "true"
    if (elem.x_triggers):
        xtriggers = {}
        for xtrigger in elem.x_triggers:
            xtriggers[xtrigger.trigger.element_id] = xtrigger.result.element_id
        content["xtriggers"] = xtriggers
    if (elem.child_slots):
        slots = []
        for slot in elem.child_slots:
            slots += [dict_slot_specification(slot)]
        content["slots"] = slots
    if (elem.no_art_needed):
        content["noartneeded"] = "true"
    if (elem.comments):
        content["comments"] = elem.comments
    if (elem.induces):
        induces = []
        for item in elem.induces:
            induction = {}
            induction["id"] = item.recipe.recipe_id
            induction["chance"] = item.chance
            induces += [induction]
        content["induces"] = induces
    return content
    
def dict_one_recipe(recipe):
    content = {}
    content["id"] = recipe.recipe_id
    if (recipe.label):
        content["label"] = recipe.label
    content["actionId"] = recipe.action.verb_id
    requirements = {}
    for req in recipe.requirements:
        requirements[req.element.element_id] = req.quantity
    content["requirements"] = requirements
    if (recipe.slot_specifications):
        slots = []
        for slot in recipe.slot_specifications:
            slots += [dict_slot_specification(slot)]
        content["slots"] = slots
    effects = {}
    for effect in recipe.effects:
        effects[effect.element.element_id] = effect.quantity
    content["effects"] = effects
    if (recipe.aspects):
        aspects = {}
        for aspect in recipe.aspects:
            aspects[aspect.element.element_id] = aspect.quantity
        content["aspects"] = aspects
    if (recipe.mutation_effects):
        mutations = []
        for mutation in recipe.mutation_effects:
            mutations += [dict_mutation_effect(mutation)]
        content["mutations"] = mutations
    content["hintonly"] = recipe.hint_only
    content["craftable"] = recipe.craftable
    if (recipe.start_description):
        content["startdescription"] = recipe.start_description
    content["description"] = recipe.description
    if (recipe.alternative_recipes):
        alternative_recipes = []
        for item in recipe.alternative_recipes:
            item_dict = {}
            item_dict["id"] = item.recipe.recipe_id
            item_dict["chance"] = item.chance
            item_dict["additional"] = item.additional
            alternative_recipes += [item_dict]
        content["alternativerecipes"] = alternative_recipes
    if (recipe.alternative_recipes):
        linked = []
        for item in recipe.linked_recipes:
            item_dict = {}
            item_dict["id"] = item.recipe.recipe_id
            item_dict["chance"] = item.chance
            item_dict["additional"] = item.additional
            linked += [item_dict]
        content["linked"] = linked
    content["warmup"] = recipe.warmup
    if (recipe.deck_effect):
        deck_effects = {}
        for effect in recipe.deck_effect:
            deck_effects[effect.deck.deck_id] = effect.quantity
        content["deckeffect"] = deck_effects
    if (recipe.signal_ending_flavour.value != "none"):
        content["signalEndingFlavour"] = recipe.signal_ending_flavour.value
    if (recipe.ending_flag):
        content["ending"] = recipe.ending_flag
    if (recipe.max_executions):
        content["maxexecutions"] = recipe.max_executions
    if (recipe.burn_image):
        content["burnimage"] = recipe.burn_image
    if (recipe.portal_effect.value != "none"):
        content["portaleffect"] = recipe.portal_effect.value
    content["signalimportantloop"] = recipe.signal_important_loop
    if (recipe.comments):
        content["comments"] = recipe.comments
    return content
    
def dict_one_verb(verb):
    content = {}
    content["id"] = verb.verb_id
    content["label"] = verb.label
    content["description"] = verb.description
    content["atStart"] = verb.at_start
    if (verb.primary_slot_specification):
        content["slots"] = [dict_slot_specification(verb.primary_slot_specification)]
    content["comments"] = verb.comments
    return content

def dict_one_deck(deck):
    content = {}
    content["id"] = deck.deck_id
    cards = []
    for card in deck.cards:
        cards += [card.element_id]
    content["spec"] = cards
    if (deck.default_card):
        content["defaultcard"] = deck.default_card.element_id
    content["resetonexhaustion"] = deck.reset_on_exhaustion
    draw_messages = {}
    default_messages = {}
    for draw_message in deck.all_draw_messages:
        if (not draw_message.default):
            draw_messages[draw_message.element.element_id] = draw_message.message
        else:
            default_messages[draw_message.element.element_id] = draw_message.message
    content["drawmessages"] = draw_messages
    content["defaultdrawmessages"] = default_messages
    content["comments"] = deck.comments
    return content
    
def dict_one_legacy(legacy):
    content = {}
    content["id"] = legacy.id
    content["label"] = legacy.label
    content["description"] = legacy.description
    content["startdescription"] = legacy.start_description
    effects = {}
    for effect in legacy.effects:
        effects[effect.element.element_id] = effect.quantity
    content["effects"] = effects
    content["image"] = legacy.image
    content["fromEnding"] = legacy.from_ending
    content["availableWithoutEndingMatch"] = legacy.available_without_ending_match
    content["comments"] = legacy.comments
    return content

def dict_slot_specification(slot):
    content = {}
    content["id"] = slot.label
    if (slot.for_verb):
        content["actionId"] = slot.for_verb.verb_id
    if (slot.required):
        required = {}
        for item in slot.required:
            required[item.element.element_id] = item.quantity
        content["required"] = required
    if (slot.forbidden):
        forbidden = {}
        for item in slot.forbidden:
            forbidden[item.element.element_id] = item.quantity
        content["forbidden"] = forbidden
    content["description"] = slot.description
    content["greedy"] = slot.greedy
    content["consumes"] = slot.consumes
    content["noanim"] = slot.no_animation
    return content
    
def dict_mutation_effect(mutation):
    content = {}
    content["filterOnAspectId"] = mutation.filter_on_aspect.element_id
    content["mutateAspectId"] = mutation.mutate_aspect.element_id
    content["mutationLevel"] = mutation.mutation_level
    content["additive"] = mutation.additive
    return content

with get_session() as session:
    bo = export_compendium(session)
    print(bo)