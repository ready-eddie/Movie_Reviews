from flask_app import app
from flask_app.controllers import users, reviews, movies


if __name__ == "__main__":
    app.secret_key = 'shhhh'
    app.run(debug=True, port=5001)
