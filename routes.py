from flask import Blueprint

routeBp = Blueprint('routes',__name__)

@routeBp.route('/')
def home():
    return 'Home'

@routeBp.route('/about')
def about():
    return 'About'
