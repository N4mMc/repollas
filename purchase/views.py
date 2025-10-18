from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import PurchaseSerializer
from .services import get_all_purchase, get_purchase_by_id, create_purchase

class PurchaseList(APIView):

    def get(self, request):
        try:
            purchases = get_all_purchase()
            serializer = PurchaseSerializer(purchases, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            purchase = create_purchase(request.data)
            serializer = PurchaseSerializer(purchase)
            if serializer.is_valid():
                serializer.save()
                return Response(status = status.HTTP_201_CREATED)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

class PurchaseDetails(APIView):

    def get(self, request, id):
        try:
            purchase = get_purchase_by_id(id)
            serializer = PurchaseSerializer(purchase)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
from django.shortcuts import render, redirect, get_object_or_404
from .models import Purchase
from .forms import PurchaseForm

def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, 'purchase/purchase_list.html', {'purchases': purchases})

def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_list')
    else:
        form = PurchaseForm()
    return render(request, 'purchase/purchase_form.html', {'form': form})

def purchase_update(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            return redirect('purchase_list')
    else:
        form = PurchaseForm(instance=purchase)
    return render(request, 'purchase/purchase_form.html', {'form': form})

def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        purchase.delete()
        return redirect('purchase_list')
    return render(request, 'purchase/purchase_delete.html', {'purchase': purchase})