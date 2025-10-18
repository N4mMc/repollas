from django.db.models import F
from django.shortcuts import get_object_or_404
from .models import Ingredient

def create_ingredient(data):
    name = data["name"]
    price_per_unit = data["price_per_unit"]
    measurament = data["measurament"]
    ingredient = Ingredient.objects.create(
        name = name,
        price_per_unit = price_per_unit,
        measurament = measurament
    )
    return ingredient

def get_all_ingredient():
    ingredients = Ingredient.objects.all()
    return ingredients

def get_ingredient_by_id(id):
    ingredient = get_object_or_404(Ingredient, pk = id)
    return ingredient

def update_ingredient(id, data):
    ingredient = get_object_or_404(Ingredient, pk=id)
    Ingredient.objects.filter(pk=id).update(price_per_unit=data["price_per_unit"])
    Ingredient.objects.filter(pk=id).update(name=data["name"])
    Ingredient.objects.filter(pk=id).update(measurament=data["measurament"])
    Ingredient.objects.filter(pk=id).update(stock=data["stock"])
    ingredient.refresh_from_db()
    return ingredient

def increase_ingredient_stock(id, amount):
    ingredient = get_object_or_404(Ingredient, pk=id)
    if ingredient.stock + amount < 0:
        raise ValueError("Stock cannot be negative")
    Ingredient.objects.filter(pk=id).update(stock=F("stock") + amount)
    ingredient.refresh_from_db()
    return ingredient

def decrease_ingredient_stock(id, amount):
    ingredient = get_object_or_404(Ingredient, pk=id)
    if ingredient.stock + amount < 0:
        raise ValueError("Stock cannot be negative")
    Ingredient.objects.filter(pk=id).update(stock=F("stock") - amount)
    ingredient.refresh_from_db()
    return ingredient