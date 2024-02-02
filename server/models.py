from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    # Fix the back_populates argument with overlaps
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza', back_populates='restaurants')
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', overlaps='pizzas')

class Pizza(db.Model):
    __tablename__ = 'pizza'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)

    # Fix the back_populates argument with overlaps
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizza', back_populates='pizzas')
    pizza_restaurants = db.relationship('RestaurantPizza', back_populates='pizza', overlaps='restaurants')

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizza'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)

    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas', overlaps='pizzas')
    pizza = db.relationship('Pizza', back_populates='pizza_restaurants', overlaps='restaurants')

    @validates('price')
    def validate_price(self, key, value):
       if not (1 <= value <= 30):
        raise ValueError("Price must be between 1 and 30.")
       return value