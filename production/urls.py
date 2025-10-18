from django.urls import path, include
from .views import ProductionList, ProductionDetail
from . import views


urlpatterns = [
    path('', views.production_list, name='production_list'),
    path('create/', views.production_create, name='production_create'),
    path('api/', ProductionList.as_view(), name='productions' ),
    path('api/<uuid:id>/', ProductionDetail.as_view(), name='production' )
]