from typing import List, Tuple, Union, Dict, Any, Optional

from sqlalchemy.orm import Session

from frangiclave.compendium.deck import Deck, DeckDrawMessage
from frangiclave.compendium.element import Element
from frangiclave.compendium.ending import Ending
from frangiclave.compendium.legacy import Legacy
from frangiclave.compendium.recipe import Recipe
from frangiclave.compendium.verb import Verb


def search_compendium(session: Session, keywords: Optional[str]) -> List[Dict[str, Any]]:
    results = []

    # Check if a set of keywords was provided
    if keywords is None:
        return results

    # Check if the processed string is empty
    search_keywords = keywords.lower().strip()
    if not search_keywords:
        return results

    deck_candidates = [
        (
            d.deck_id,
            d.label,
            d.description,
            *[dm.message for dm in d.all_draw_messages],
            d.comments
        )
        for d in session.query(Deck).all()
    ]
    results += _find_results(search_keywords, 'deck', deck_candidates)
    element_candidates = session.query(
        Element.element_id,
        Element.label,
        Element.description,
        Element.uniqueness_group,
        Element.comments
    ).all()
    results += _find_results(search_keywords, 'element', element_candidates)
    ending_candidates = session.query(
        Ending.ending_id,
        Ending.description,
        Ending.title
    ).all()
    results += _find_results(search_keywords, 'ending', ending_candidates)
    legacy_candidates = session.query(
        Legacy.legacy_id,
        Legacy.label,
        Legacy.description,
        Legacy.start_description,
        Legacy.comments
    ).all()
    results += _find_results(search_keywords, 'legacy', legacy_candidates)
    recipe_candidates = session.query(
        Recipe.recipe_id,
        Recipe.label,
        Recipe.start_description,
        Recipe.description,
        Recipe.comments
    ).all()
    results += _find_results(search_keywords, 'recipe', recipe_candidates)
    verb_candidates = session.query(
        Verb.verb_id,
        Verb.label,
        Verb.description,
        Verb.comments,
    ).all()
    results += _find_results(search_keywords, 'verb', verb_candidates)
    return results


def search_compendium_by_id(session: Session, item_id: str) -> Optional[Any]:
    results = []
    results += session.query(Deck).filter(Deck.deck_id.contains(item_id)).all()
    results += session.query(Element).filter(Element.element_id.contains(item_id)).all()
    results += session.query(Ending).filter(Ending.ending_id.contains(item_id)).all()
    results += session.query(Legacy).filter(Legacy.legacy_id.contains(item_id)).all()
    results += session.query(Recipe).filter(Recipe.recipe_id.contains(item_id)).all()
    results += session.query(Verb).filter(Verb.verb_id.contains(item_id)).all()

    if not results:
        return None

    best_candidate = None
    best_candidate_id = None
    for result in results:
        if isinstance(result, Deck):
            result_id = result.deck_id
        elif isinstance(result, Element):
            result_id = result.element_id
        elif isinstance(result, Ending):
            result_id = result.ending_id
        elif isinstance(result, Legacy):
            result_id = result.legacy_id
        elif isinstance(result, Recipe):
            result_id = result.recipe_id
        elif isinstance(result, Verb):
            result_id = result.verb_id
        else:
            continue

        # Return exact matches immediately
        if result_id == item_id:
            return result

        # Return the closest match in terms of length otherwise
        if not best_candidate or len(result_id) < len(best_candidate_id):
            best_candidate = result
            best_candidate_id = result_id

    return best_candidate


def _find_results(
        keywords: str,
        _type: str,
        candidates: List[Tuple[Union[int, str]]]
) -> List[Dict[str, Any]]:
    results = []
    for candidate in candidates:
        matches = []
        for field in candidate:
            if not field:
                continue
            start = field.lower().find(keywords)
            if start < 0:
                continue
            end = start + len(keywords)
            match = (
                    ('...' if start > 30 else '')
                    + field[max(0, start - 30):start].lstrip()
                    + field[start:end]
                    + field[end:end+30].rstrip()
                    + ('...' if len(field) - end > 30 else '')
            )
            matches.append(match)
        if matches:
            results.append({
                'id': candidate[0],
                'type': _type,
                'matches': matches
            })
    return results
