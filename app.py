from flask import Flask
from routes import routeBp
from auth import authBp


app = Flask(__name__)
app.secret_key = "Qwertyu"
app.register_blueprint(routeBp)
app.register_blueprint(authBp)

if __name__ == "__main__":
    app.run(debug=True)