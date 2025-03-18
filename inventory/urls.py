from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.add_ingredient, name='add_ingredient'),
    path('add-menu-item/', views.add_menu_item, name='add_menu_item'),
path('add-sale/', views.add_sale, name='add_sale'),
]