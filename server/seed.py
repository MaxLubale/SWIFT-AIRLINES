from app import db, Restaurant, Pizza, RestaurantPizza

def seed_data():
    # Create sample data
    restaurant1 = Restaurant(name='Sottocasa NYC', address='298 Atlantic Ave, Brooklyn, NY 11201')
    restaurant2 = Restaurant(name='PizzArte', address='69 W 55th St, New York, NY 10019')

    pizza1 = Pizza(name='Cheese', ingredients='Dough, Tomato Sauce, Cheese')
    pizza2 = Pizza(name='Pepperoni', ingredients='Dough, Tomato Sauce, Cheese, Pepperoni')

    db.session.add_all([restaurant1, restaurant2, pizza1, pizza2])
    db.session.commit()

    # Associate pizzas with restaurants
    restaurant1.pizzas.extend([pizza1, pizza2])
    restaurant2.pizzas.append(pizza2)

    # Create RestaurantPizza instances with prices
    restaurant_pizza1 = RestaurantPizza(price=15,restaurant=[0], pizzaid=[0])
    restaurant_pizza2 = RestaurantPizza(price=20,restaurant=[0], pizzaid=[1],)
    restaurant_pizza3 = RestaurantPizza(price=25,restaurant=[1], pizzaid=[1])

    db.session.add_all([restaurant_pizza1, restaurant_pizza2, restaurant_pizza3])
    db.session.commit()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        db.create_all()
        seed_data()


print("🦸‍♀️ Done seeding!")