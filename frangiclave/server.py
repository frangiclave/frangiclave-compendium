from collections import OrderedDict, defaultdict
from os.path import abspath, dirname, join

from flask import Flask, render_template, abort
from sqlalchemy.orm.exc import NoResultFound

from frangiclave.compendium.base import get_session
from frangiclave.compendium.deck import Deck
from frangiclave.compendium.file import File, FileCategory
from frangiclave.unity.importer import import_game_data

ROOT_DIR = abspath(dirname(__file__))
STATIC_DIR = join(ROOT_DIR, 'static')
TEMPLATE_DIR = join(ROOT_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)


@app.route('/')
def index():
    return render_template('index.tpl.html')


@app.route('/load/')
def load():
    import_game_data(r'C:\Program Files (x86)\Steam\steamapps\common\Cultist Simulator\cultistsimulator_Data\StreamingAssets\content\core')
    return ''


@app.route('/save/')
def save():
    pass


@app.route('/file_add/', methods=['POST'])
def file_add():
    pass


@app.route('/file_rename/', methods=['POST'])
def file_edit():
    pass


@app.route('/file_delete/', methods=['POST'])
def file_delete():
    pass


@app.route('/deck/<string:deck_id>/')
def deck(deck_id: str):
    with get_session() as session:
        return render_template(
            'deck.tpl.html',
            deck=Deck.get_by_deck_id(session, deck_id),
            show_decks=True
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
        decks = session.query(Deck.deck_id, Deck.file_id).order_by(
            Deck.deck_id).all()
        for file in file_list:
            files[file.category.value][file] = [
                deck_id for deck_id, file_id in decks if file_id == file.id
            ]
        session.expunge_all()
    return dict(
        files=files,
        read_only=app.config['READ_ONLY'],
        decks_open=False,
        elements_open=False,
        recipes_open=False,
        verbs_open=False
    )
