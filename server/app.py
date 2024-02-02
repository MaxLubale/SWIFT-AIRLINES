from flask import Flask, request, jsonify
from models import db, Restaurant, Pizza, RestaurantPizza
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurant.db'
db.init_app(app)
migrate = Migrate(app, db)

# Routes

@app.route('/')
def home():
    return '<h1>Welcome to restaurants pizzas API</h1>'
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    data = [{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants]
    return jsonify(data)

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': [{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in restaurant.pizzas]
        }
        return jsonify(data)
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        # Delete associated RestaurantPizzas
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
        # Delete the restaurant
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    data = [{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizzas]
    return jsonify(data)

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    try:
        restaurant_pizza = RestaurantPizza(price=data['price'], pizza_id=data['pizza_id'], restaurant_id=data['restaurant_id'])
        db.session.add(restaurant_pizza)
        db.session.commit()
        pizza = Pizza.query.get(data['pizza_id'])
        return jsonify({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients})
    except Exception as e:
        return jsonify({'errors': [str(e)]}), 400

if __name__ == '__main__':
    app.run(debug=True)
