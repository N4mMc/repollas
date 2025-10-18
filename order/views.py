from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import OrderSerializer
from .services import create_order, get_all_orders, get_order_by_id

class OrderList(APIView):

    def get(self, request):
        try:
            orders = get_all_orders()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            order = create_order(request.data)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):

    def get(self, reqeust, id):
        try:
            order = get_order_by_id(id)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
from django.shortcuts import render, redirect
from .models import Order
from ingredient.models import Ingredient

# 📋 Lista de órdenes
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'order/order_list.html', {'orders': orders})

# ➕ Crear nueva orden
from django.shortcuts import render, redirect
from ingredient.models import Ingredient
from .services import create_order

def order_create(request):
    ingredients = Ingredient.objects.all()

    if request.method == 'POST':
        # Recibir ingredientes seleccionados
        ingredient_ids = request.POST.getlist('ingredient_id[]')
        quantities = request.POST.getlist('quantity[]')
        costs = request.POST.getlist('cost[]')

        data = []
        for i in range(len(ingredient_ids)):
            if ingredient_ids[i]:
                data.append({
                    'ingredient_id': ingredient_ids[i],
                    'quantity': int(quantities[i]),
                    'const': float(costs[i]),
                })

        order = create_order(data)
        return redirect('order_list')

    return render(request, 'order/order_form.html', {'ingredients': ingredients})