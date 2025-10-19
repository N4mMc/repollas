from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import IngredientSerializer
from .services import update_ingredient, create_ingredient, get_all_ingredient, get_ingredient_by_id
from .models import Ingredient

#API views
class IngredientList(APIView): 

    def get(self, request):
        try:
            ingredients = get_all_ingredient()
            serializer = IngredientSerializer(ingredients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            ingredient = create_ingredient(request.data)
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class IngredientDetail(APIView):

    def get(self, request, id):
        try:
            ingredient = get_ingredient_by_id(id)
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            ingredient = update_ingredient(id, request.data)
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

#html views  
from .forms import IngredientForm

# Lista de ingredientes
def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient/ingredient_list.html', {'ingredients': ingredients})

# Crear ingrediente
def ingredient_create(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()  # guardamos y obtenemos el objeto creado
            # Redirigir al template de confirmación
            return render(request, 'ingredient/ingredient_created.html', {'ingredient': ingredient})
    else:
        form = IngredientForm()
    return render(request, 'ingredient/ingredient_form.html', {'form': form})

# Editar ingrediente
def ingredient_update(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, 'ingredient/ingredient_form.html', {'form': form})

# Eliminar ingrediente
def ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredient_list')
    return render(request, 'ingredient/ingredient_confirm_delete.html', {'ingredient': ingredient})