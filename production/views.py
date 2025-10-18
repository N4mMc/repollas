from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from .serializer import ProductionSerializer
from .services import get_all_productions, get_production_by_id, create_production
from item_used.services import create_item_used
from ingredient.services import get_all_ingredient


class ProductionList(APIView):

    def get(self, request):
        try:
            productions = get_all_productions()
            serializer = ProductionSerializer(productions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            production = create_production(request.data)
            serializer = ProductionSerializer(production)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

class ProductionDetail(APIView):

    def get(self, request, id):
        try:
            production = get_production_by_id(id)
            serializer = ProductionSerializer(production)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
from django.shortcuts import render, redirect
from .models import Production

# 📋 Lista de producciones
def production_list(request):
    productions = get_all_productions().order_by('-created_at')
    return render(request, 'production/production_list.html', {'productions': productions})

# ➕ Crear nueva producción
def production_create(request):
    ingredients  = get_all_ingredient()
    if request.method == 'POST':
        repollas = int(request.POST.get('repollas', 0))
        sales = float(request.POST.get('sales', 0))
        boxes =  round(repollas / 6)
        ingredient_ids = request.POST.getlist('ingredient_id[]')
        quantities = request.POST.getlist('quantity[]')
        items_used_list = []
        for i in range(len(ingredient_ids)):
            if ingredient_ids[i]:
                item = create_item_used(
                    int(quantities[i]),
                    ingredient_ids[i]
                )
                items_used_list.append(item.id)
        data = {
            'repollas': repollas,
            'boxes': boxes,
            'sales': sales,
            'item_used': items_used_list
        } 
        create_production(data)
        return redirect('production_list')
    return render(request, 'production/production_form.html', {'ingredients': ingredients})
