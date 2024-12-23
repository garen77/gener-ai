from flask import (Blueprint, request, session, jsonify)
from flask_cors import (CORS, cross_origin)
from db import get_db

authBp = Blueprint('auth',__name__)
CORS(authBp, resources={r"/*": {"origins": "*"}})

@authBp.route('/login', methods=['GET', 'POST'])
@cross_origin()
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
            email = ''
            if "email" in user:
                email = user['email']
            response = jsonify({'username': user['name'], 'email': email})
            return response
    return error

@authBp.route('/logout')
def logout():
    session.pop('loggedIn', None)
    session.pop('username', None)

@authBp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    db = get_db()
    userCollection = db['user']
    user = userCollection.find_one({"name": username})
    user_email = userCollection.find_one({"email": email})
    if user is not None:
        return f"Utente con username {username} gia' censito"
    elif user_email is not None:
        return f"Utente con email {email} gia' censito"
    else:
        userCollection.insert_one({'name': username, 'password': password, 'email': email})
        return f"Utente {username} censito con successo!!"