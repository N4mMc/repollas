from item_used.services import get_item_used_by_id
from .models import Production

def create_production(data):
    production = Production.objects.create(
        repollas=data.get("repollas", 0),
        boxes=data.get("boxes", 0),
        sales=data.get("sales", 0)
    )
    production.item_used.set(data['item_used'])
    return production

def get_all_productions():
    productions = Production.objects.all()
    return productions

def get_production_by_id(id):
    production = Production.objects.get(pk = id)
    return production