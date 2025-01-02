from flask import (Blueprint, request)
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

@routeBp.route('/update-game-user', methods=['POST'])
def updateGameUser():
    db = get_db()
    gamesCollection = db['game']
    userCollection = db['user']
    userName = request.form['userName']
    gameName = request.form['gameName']

    error = None
    
    if not userName:
        error = 'User name is required.'
    elif not gameName:
        error = 'Game name is required.'
    if error is None:
        user = userCollection.find_one({"name": userName})
        game = gamesCollection.find_one({"name": gameName})
        if not user:
            error = f"Utente con username {userName} inesistente"
        elif not game:
            error = f"Gioco {gameName} inesistente."
        if not error:
            gamesCollection.update_one({ 'name': gameName }, { '$push': {'users': user['_id']}})
            return f"Utente {userName} censito con successo nel gioco {gameName} !!"
        return error
    
@routeBp.route('/')
def home():
    return 'Home'

@routeBp.route('/about')
def about():
    return 'About'
