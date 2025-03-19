from django.shortcuts import render, redirect
from .models import Ingredient, MenuItem, Sale, RecipeRequirement, Order, OrderItem
from .forms import IngredientForm, MenuItemForm, SaleForm, LocationForm, EmployeeForm, OrderForm
from django.contrib import messages
from django.db.models import Sum

def inventory_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'inventory/inventory_list.html', {'ingredients': ingredients})

def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ingredient added successfully!")
            return redirect('inventory_list')
    else:
        form = IngredientForm()
    return render(request, 'inventory/add_ingredient.html', {'form': form})

def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item added successfully!")
            return redirect('inventory_list')
    else:
        form = MenuItemForm()
    return render(request, 'inventory/add_menu_item.html', {'form': form})

def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save()

            for req in sale.menu_item.reciperequirement_set.all():
                ingredient = req.ingredient
                ingredient.available_quantity -= req.quantity_required * sale.quantity_sold
                ingredient.save()

            messages.success(request, "Sale recorded successfully!")
            return redirect('inventory_list')
    else:
        form = SaleForm()
    return render(request, 'inventory/add_sale.html', {'form': form})

def sales_report(request):
    sales = Sale.objects.all()
    total_sales = sales.aggregate(Sum('quantity_sold'))
    return render(request, 'inventory/sales_report.html', {'sales': sales, 'total_sales': total_sales})

"""@login_required"""
def add_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            for item in request.POST.getlist('order_items'):
                order_item = OrderItem.objects.create(order=order, menu_item=MenuItem.objects.get(id=item['menu_item']), quantity=item['quantity'])
            order.calculate_total()
            return redirect('order_list')
    else:
        order_form = OrderForm()
    return render(request, 'inventory/add_order.html', {'order_form': order_form})


"""@login_required"""
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'inventory/order_list.html', {'orders': orders})


"""@login_required"""
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'inventory/add_employee.html', {'form': form})


"""@login_required"""
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')
    else:
        form = LocationForm()
    return render(request, 'inventory/add_location.html', {'form': form})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect or return a response
    else:
        form = OrderForm()
    return render(request, 'inventory/create_order.html', {'form': form})