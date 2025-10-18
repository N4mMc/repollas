from django.urls import path
from .views import OrderList, OrderDetail
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('api/', OrderList.as_view(), name='orders'),
    path('api/<uuid:id>/', OrderDetail.as_view(), name='order')
]
