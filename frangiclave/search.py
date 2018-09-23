from typing import List, Tuple, Union, Dict, Any, Optional

from sqlalchemy.orm import Session

from frangiclave.compendium.deck import Deck
from frangiclave.compendium.element import Element
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

    deck_candidates = session.query(
        Deck.deck_id,
        Deck.label,
        Deck.description,
        Deck.comments
    ).all()
    results += _find_results(search_keywords, 'deck', deck_candidates)
    element_candidates = session.query(
        Element.element_id,
        Element.label,
        Element.description,
        Element.comments
    ).all()
    results += _find_results(search_keywords, 'element', element_candidates)
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


def _find_results(
        keywords: str,
        _type: str,
        candidates: List[Tuple[Union[int, str]]]
) -> List[Dict[str, Any]]:
    results = []
    for candidate in candidates:
        matches = []
        for field in candidate[1:]:
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
