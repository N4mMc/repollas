from django.urls import path
from .views import ItemUsedList, ItemUsedDetails
from . import views

urlpatterns = [
    path('', views.item_used_list, name='item_used_list'),
    path('create/', views.item_used_create, name='item_used_create'),
    path('api/', ItemUsedList.as_view(), name='itemsused' ),
    path('api/<uuid:id>/', ItemUsedDetails.as_view(), name='itemused' )
    ]