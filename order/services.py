from ingredient.services import get_ingredient_by_id, increase_ingredient_stock
from purchase.services import create_purchase
from .models import Order

def create_order(data):
    order = Order.objects.create()
    total = 0
    for purchase in data:
        ingredient = get_ingredient_by_id(purchase["ingredient_id"])
        quantity = purchase["quantity"]
        cost = purchase["const"]
        total += cost
        purchase = create_purchase(quantity, cost, order, ingredient)
        if purchase:
            increase_ingredient_stock(ingredient.id, quantity)
    order.total = total
    order.save()
    return order

def get_all_orders():
    orders = Order.objects.all()
    return orders

def get_order_by_id(id):
    order = Order.objects.get(Order, pk = id)
    return order