from flask import Blueprint, render_template, request, redirect

from models.base import Session
from models.pizza import Pizza
from models.ingredient import Ingredient
from data.wheather import get_wheather
from flask import render_template
from flask import Flask, url_for, redirect


pizza_route = Blueprint("pizzas", __name__)


@pizza_route.get("/")
def index():
    wheather = get_wheather("Neratovice")
    temp = wheather.get("temp")
    pizza_name = "Невідома піцца"
    if temp is not None:
        if 26 > temp > 10:
            pizza_name = "Тепла"
        elif temp <= 10:
            pizza_name = "Холодна"
        elif temp > 26:
            pizza_name = "Пепероні"


    return render_template("index.html", title="Моя супер піцерія", wheather=wheather, pizza_name=pizza_name)


@pizza_route.get("/menu/")
def menu():
    wheather = get_wheather("Kyiv")
    with Session() as session:
        pizzas = session.query(Pizza).all()
        ingredients = session.query(Ingredient).all()

        context = {
            "pizzas": pizzas,
            "ingredients": ingredients,
            "title": "Мега меню",
            "wheather": wheather
        }
        return render_template("menu.html", **context)


@pizza_route.post("/add_pizza/")
def add_pizza():
    with Session() as session:
        name = request.form.get("name")
        price = request.form.get("price")
        ingredients = request.form.getlist("ingredients")
        ingredients = session.query(Ingredient).where(Ingredient.id.in_(ingredients)).all()

        pizza = Pizza(name=name, price=price, ingredients=ingredients)
        session.add(pizza)
        session.commit()
        return redirect("/menu/")
    


@pizza_route.get("/pizza/del/<int:id>/")
def del_pizza(id):
    with Session() as session:
        pizza = session.query(Pizza).where(Pizza.id == id).first()
        session.delete(pizza)
        session.commit()
        return redirect(url_for("pizzas.menu"))


@pizza_route.get("/pizza/edit/<int:id>/")
@pizza_route.post("/pizza/edit/<int:id>/")
def edit_pizza(id):
    with Session() as session:
        pizza = session.query(Pizza).where(Pizza.id == id).first()
        if request.method == "POST":
            title = request.form.get("title")
            text = request.form.get("text")

            pizza.title = title
            pizza.text = text
            session.commit()
            return redirect(url_for("pizza.index"))

        return render_template("edit_pizza.html", pizza=pizza)