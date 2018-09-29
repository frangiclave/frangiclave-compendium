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
        session.query(Deck, Deck.file_id)
        .order_by(Deck.deck_id)
        .all()
    )
    elements = (
        session.query(Element, Element.file_id)
        .order_by(Element.element_id)
        .all()
    )
    legacies = (
        session.query(Legacy, Legacy.file_id)
        .order_by(Legacy.legacy_id)
        .all()
    )
    recipes = (
        session.query(Recipe, Recipe.file_id)
        .order_by(Recipe.recipe_id)
        .all()
    )
    verbs = (
        session.query(Verb, Verb.file_id)
        .order_by(Verb.verb_id)
        .all()
    )
    items = decks + elements + legacies + recipes + verbs
    for file in file_list:
        files[file.category.value][file] = [
            item for item, file_id in items if file_id == file.id
        ]
    #export_elements(files["elements"])
    #export_recipes(files["recipes"])
    for category in files:
        if category == "elements":
            export_elements(files[category])
        else:
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
    return True

def dict_one_item(item, category):
    if category == "recipes":
        return dict_one_recipe(item)
    elif category == "verbs":
        return dict_one_verb(item)
    elif category == "decks":
        return dict_one_deck(item)
    elif category == "legacies":
        return dict_one_legacy(item)
    else:
        print("Wrong category")
        return None
    
def export_elements(element_files: OrderedDict) -> Any:
    for file in element_files:
        print("exporting elements " + file.name)
        if file.category.value != "elements":
            print("NOT AN ELEMENT WHAT ARE YOU DOING")
            print (file.category.value)
            return False
        content = "{\"elements\": [\n\t"
        for elem in element_files[file]:
            content += export_one_element(elem)
        
        content = content[:-3]
        content += "]}"
        game_dir_base = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Cultist Simulator\\"
        game_dir_cont = "cultistsimulator_Data\\StreamingAssets\\content\\"
        f = open(game_dir_base + game_dir_cont + file.group.value + "\\" + file.category.value + "\\" + file.name, "w")
        f.write(content)
        f.close()

def export_one_element(elem):
    content = "{id:" + elem.element_id + ",\n\t"
    if (elem.label):
        content += "label:\"" + elem.label + "\",\n\t"
    if (elem.description):
        content += "description: \"" + repr(elem.description)[1:-1] + "\",\n\t"
    if (elem.aspects):
        content += "aspects: {"
        for aspect in elem.aspects:
            content += aspect.aspect.element_id + ": "
            content += str(aspect.quantity) + ", "
        content = content[:-2] #strip last comma
        content += "},\n\t"
    if (elem.animation_frames != 0):
        content += "animFrames:" + str(elem.animation_frames) + ",\n\t"
    if (elem.icon):
        content += "icon:" + str(elem.icon) + ",\n\t"
    if (elem.lifetime != 0):
        content += "lifetime:" + str(elem.lifetime) + ",\n\t"
    if (elem.unique):
        content += "unique: true,\n\t"
    if (elem.decay_to):
        content += "decay_to:" + str(elem.decay_to.element_id) + ",\n\t"
    if (elem.is_aspect):
        content += "isAspect: true,\n\t"
    if (elem.x_triggers):
        content += "xtriggers: {"
        for xtrigger in elem.x_triggers:
            content += xtrigger.trigger.element_id + ": "
            content += xtrigger.result.element_id + ", "
        content = content[:-2] #strip last comma
        content += "},\n\t"
    if (elem.child_slots):
        content += "slots: ["
        for slot in elem.child_slots:
            content += export_slot_specification(slot)
        content = content[:-4]
        content += "],\n\t"
    if (elem.no_art_needed):
        content += "noartneeded: true\n\t"
    if (elem.comments):
        content += "comments: \"" + elem.comments + "\",\n\t"
    if (elem.induces):
        content += "induces: ["
        for item in elem.induces:
            content += "{id:\"" + item.recipe.recipe_id + "\", chance:" + str(item.chance) + "},"
        content = content[:-1]
        content += "],\n\t"
    content = content[:-3] + "\n\t"
    content += "},\n\t"
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
    
def export_slot_specification(slot):
    content = "{id:\"" + slot.label + "\","
    if (slot.for_verb):
        content += "actionID:\"" + slot.for_verb.verb_id + "\","
    if (slot.required):
        content += "required: {"
        for item in slot.required:
            content += item.element.element_id + ": " + str(item.quantity) + ","
        if content[-1] == ',':
            content = content[:-1]
        content += "},"
    if (slot.forbidden):
        content += "forbidden: {"
        for item in slot.forbidden:
            content += item.element.element_id + ": " + str(item.quantity) + ","
        content += "},"
    if (slot.description):
        content += "description:\"" + slot.description + "\","
    if (slot.greedy):
        content += "greedy:true,"
    if (slot.consumes):
        content += "consumes:true,"
    if (slot.no_animation):
        content += "noanim:true,"
    content = content[:-1]
    content += "},\n\t\t"
    return content

def dict_slot_specification(slot):
    content = {}
    content["id"] = slot.label
    if (slot.for_verb):
        content["actionID"] = slot.for_verb.verb_id
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
    return content

with get_session() as session:
    bo = export_compendium(session)
    print(bo)