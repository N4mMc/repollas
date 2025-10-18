from django.shortcuts import get_object_or_404
from .models import Purchase

def create_purchase(quantity, cost, order, ingredient):
    purchase = Purchase.objects.create(
        quantity = quantity,
        cost = cost,
        order = order,
        ingredient = ingredient
    )
    return purchase

def get_all_purchase():
    purchases = Purchase.objects.all()
    return purchases

def get_purchase_by_id(id):
    purchase = get_object_or_404(Purchase, pk = id)
    return purchase