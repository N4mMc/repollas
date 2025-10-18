from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ItemUsedSerializer
from .services import get_items_used, get_item_used_by_id, create_item_used
from ingredient.services import get_all_ingredient, get_ingredient_by_id
from django.shortcuts import render, redirect
from production.services import get_all_productions, get_production_by_id

class ItemUsedList(APIView):

    def get(self, request):
        try:
            items_used = get_items_used()
            serialzier = ItemUsedSerializer(items_used, many=True)
            return Response(serialzier.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, ingredient_id):
        try:
            item_used = create_item_used(request.data, ingredient_id)
            serializer = ItemUsedSerializer(item_used)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
class ItemUsedDetails(APIView):

    def get(self, request, id):
        try:
            item_used = get_item_used_by_id(id)
            serializer = ItemUsedSerializer(item_used)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        

from django.shortcuts import render, redirect
from .models import ItemUsed

# Listar items usados
def item_used_list(request):
    items = ItemUsed.objects.select_related('ingredient').all()
    return render(request, 'item_used/item_used_list.html', {'items': items})

# Crear nuevo item usado
def item_used_create(request):
    ingredients = get_all_ingredient()
    productions = get_all_productions()

    if request.method == 'POST':
        ingredient_id = request.POST.get('ingredient')
        production_id = request.POST.get('production')
        quantity = int(request.POST.get('quantity'))
        if ingredient_id and production_id and quantity:
            item = create_item_used(quantity, ingredient_id)
            production = get_production_by_id(production_id)
            production.item_used.add(item)
            return redirect('item_used_list')

    return render(request, 'item_used/item_used_form.html', {
        'ingredients': ingredients,
        'productions': productions
    })
