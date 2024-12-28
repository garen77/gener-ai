from flask import (Blueprint, jsonify)
from flask_cors import (CORS, cross_origin)
from db import get_db
from bson import json_util

routeBp = Blueprint('routes',__name__)


CORS(routeBp, resources={r"/*": {"origins": "*"}})

@routeBp.route('/games-list', methods=['POST'])
@cross_origin()
def games_list():
    db = get_db()
    gamesCollection = db['game']
    games = json_util.dumps(gamesCollection.find({}))
    return games


@routeBp.route('/')
def home():
    return 'Home'

@routeBp.route('/about')
def about():
    return 'About'
