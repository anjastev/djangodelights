from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.add_ingredient, name='add_ingredient'),
    path('add-menu-item/', views.add_menu_item, name='add_menu_item'),
    path('add-sale/', views.add_sale, name='add_sale'),
    path('sales-report/', views.sales_report, name='sales_report'),
    path('add-order/', views.add_order, name='add_order'),
    path('order-list/', views.order_list, name='order_list'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('add-location/', views.add_location, name='add_location'),
]