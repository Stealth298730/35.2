from flask import Flask

from routes.pizza import pizza_route
from models.pizza import Pizza
from models.ingredient import Ingredient
from models.base import create_db


app = Flask(__name__)
app.register_blueprint(pizza_route)


if __name__ == "__main__":
    create_db()
    app.run(debug=True)