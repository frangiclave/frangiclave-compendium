import re
from collections import OrderedDict, defaultdict
from os.path import abspath, dirname, join

from flask import Flask, render_template, abort, request
from markupsafe import Markup
from sqlalchemy.orm.exc import NoResultFound

from frangiclave.compendium.base import get_session
from frangiclave.compendium.deck import Deck
from frangiclave.compendium.element import Element
from frangiclave.compendium.ending import Ending
from frangiclave.compendium.file import File
from frangiclave.compendium.legacy import Legacy
from frangiclave.compendium.recipe import Recipe
from frangiclave.compendium.verb import Verb
from frangiclave.game.importer import import_game_data
from frangiclave.search import search_compendium

ROOT_DIR = abspath(dirname(__file__))
STATIC_DIR = join(ROOT_DIR, 'static')
TEMPLATE_DIR = join(ROOT_DIR, 'templates')
SPRITE_PATTERN = re.compile(r'<sprite name=([a-z]+)>')

app = Flask(__name__, template_folder=TEMPLATE_DIR)


@app.route('/')
def index():
    return render_template('index.tpl.html')


@app.route('/load/')
def load():
    if app.config['READ_ONLY']:
        abort(403)
    import_game_data(app.config['GAME_DIRECTORY'])
    return 'Game data loaded.'


@app.route('/save/')
def save():
    if app.config['READ_ONLY']:
        abort(403)
    return 'Game data saved.'


@app.route('/file_add/', methods=['POST'])
def file_add():
    pass


@app.route('/file_rename/', methods=['POST'])
def file_edit():
    pass


@app.route('/file_delete/', methods=['POST'])
def file_delete():
    pass


@app.route('/search/')
def search():
    keywords = request.args.get('keywords', '')
    with get_session() as session:
        results = search_compendium(session, keywords)
        return render_template(
            'search.tpl.html',
            keywords=keywords,
            results=results
        )


@app.route('/deck/<string:deck_id>/')
def deck(deck_id: str):
    with get_session() as session:
        return render_template(
            'deck.tpl.html',
            deck=Deck.get_by_deck_id(session, deck_id),
            show_decks=True
        )


@app.route('/element/<string:element_id>/')
def element(element_id: str):
    with get_session() as session:
        return render_template(
            'element.tpl.html',
            element=Element.get_by_element_id(session, element_id),
            show_elements=True
        )


@app.route('/ending/<string:ending_id>/')
def ending(ending_id: str):
    with get_session() as session:
        return render_template(
            'ending.tpl.html',
            ending=Ending.get_by_ending_id(session, ending_id),
            show_endings=True
        )


@app.route('/legacy/<string:legacy_id>/')
def legacy(legacy_id: str):
    with get_session() as session:
        return render_template(
            'legacy.tpl.html',
            legacy=Legacy.get_by_legacy_id(session, legacy_id),
            show_legacies=True
        )


@app.route('/recipe/<string:recipe_id>/')
def recipe(recipe_id: str):
    with get_session() as session:
        return render_template(
            'recipe.tpl.html',
            recipe=Recipe.get_by_recipe_id(session, recipe_id),
            show_recipes=True
        )


@app.route('/verb/<string:verb_id>/')
def verb(verb_id: str):
    with get_session() as session:
        return render_template(
            'verb.tpl.html',
            verb=Verb.get_by_verb_id(session, verb_id),
            show_verbs=True
        )


@app.errorhandler(NoResultFound)
def handle_invalid_usage(error):
    return page_not_found(error)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.tpl.html'), 404


@app.context_processor
def add_global_variables():
    with get_session() as session:
        file_list = session.query(File).order_by(File.name).all()
        files = defaultdict(lambda: OrderedDict())
        decks = (
            session.query(Deck.deck_id, Deck.file_id)
            .order_by(Deck.deck_id)
            .all()
        )
        elements = (
            session.query(Element.element_id, Element.file_id)
            .order_by(Element.element_id)
            .all()
        )
        endings = [
            e for e, in session
            .query(Ending.ending_id)
            .order_by(Ending.ending_id)
            .all()
        ]
        legacies = (
            session.query(Legacy.legacy_id, Legacy.file_id)
            .order_by(Legacy.legacy_id)
            .all()
        )
        recipes = (
            session.query(Recipe.recipe_id, Recipe.file_id)
            .order_by(Recipe.recipe_id)
            .all()
        )
        verbs = (
            session.query(Verb.verb_id, Verb.file_id)
            .order_by(Verb.verb_id)
            .all()
        )
        items = decks + elements + legacies + recipes + verbs
        for file in file_list:
            files[file.category.value][file] = [
                item_id for item_id, file_id in items if file_id == file.id
            ]
        session.expunge_all()
    return dict(
        base_url=app.config['BASE_URL'],
        path=request.path,
        files=files,
        endings=endings,
        read_only=app.config['READ_ONLY'],
        decks_open=False,
        elements_open=False,
        endings_open=False,
        legacies_open=False,
        recipes_open=False,
        verbs_open=False
    )


@app.template_filter('sprite_replace')
def sprite_replace(text):
    return Markup(SPRITE_PATTERN.sub(
        lambda m: r'<img src="'
                  + app.config['BASE_URL']
                  + '/static/images/icons40/aspects/'
                  + m.group(1)
                  + r'.png" width="30" height="30" />',
        text))
