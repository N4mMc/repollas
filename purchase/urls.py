from django.urls import path
from .views import PurchaseList, PurchaseDetails
from . import views

urlpatterns = [
    # Funciones
    path('', views.purchase_list, name='purchase_list'),
    path('new/', views.purchase_create, name='purchase_create'),
    path('edit/<uuid:pk>/', views.purchase_update, name='purchase_update'),
    path('delete/<uuid:pk>/', views.purchase_delete, name='purchase_delete'),

    # Clases
    path('api/', PurchaseList.as_view(), name='purchases'),
    path('api/<uuid:id>/', PurchaseDetails.as_view(), name='purchase'),
]
