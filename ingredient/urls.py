from django.urls import path
from . import views
from .views import IngredientList, IngredientDetail

urlpatterns = [
    path('', views.ingredient_list, name='ingredient_list'),
    path('create/', views.ingredient_create, name='ingredient_create'),
    path('<uuid:pk>/update/', views.ingredient_update, name='ingredient_update'),
    path('<uuid:pk>/delete/', views.ingredient_delete, name='ingredient_delete'),

    path('api/', IngredientList.as_view(), name='ingredients'),
    path('api/<uuid:id>/', IngredientDetail.as_view(), name='ingredient'),
]
