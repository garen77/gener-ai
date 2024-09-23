from flask import (Blueprint, request, session, jsonify)
from db import get_db

authBp = Blueprint('auth',__name__)

@authBp.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    args = request.args
    if request.method == 'GET':        
        username = args.get('username')
        password = args.get('password')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    userCollection = db['user']

    error = None
    
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Pasword is required.'
    
    if error is None:
        user = userCollection.find_one({"name": username})
        if not user:
            error = "Utente inesistente."
        print('User : ')
        print(user)
        if not error and password != user['password']:
            error = "Password errata."
        if not error:
            session['loggedIn'] = True
            session['username'] = user['name']
            response = jsonify({'username': user['name'], 'code': user['code']})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    return error

@authBp.route('/logout')
def logout():
    session.pop('loggedIn', None)
    session.pop('username', None)

@authBp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    code = request.form['code']
    password = request.form['password']
    db = get_db()
    userCollection = db['user']
    user = userCollection.find_one({"name": username})
    user_code = userCollection.find_one({"code": code})
    if user is not None:
        return f"Utente {username} gia' censito"
    elif user_code is not None:
        return f"Utente con codice {code} gia' censito"
    else:
        userCollection.insert_one({'name': username, 'password': password, 'code': code})
        return f"Utente {username} censito con successo!!"