from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ItemUsed
from ingredient.services import decrease_ingredient_stock, get_ingredient_by_id

def create_item_used(quantity, ingredient_id):
    ingredient = get_ingredient_by_id(ingredient_id)
    if ingredient.stock < quantity:
        raise ValueError("Not enough stock to use this ingredient.")
    item_used = ItemUsed.objects.create(
        ingredient = ingredient,
        quantity = quantity
    )
    decrease_ingredient_stock(ingredient_id, quantity)
    return item_used

def get_items_used():
    items_used = ItemUsed.objects.all()
    return items_used

def get_item_used_by_id(id):
    item_used = get_object_or_404(ItemUsed, pk=id)
    return item_used