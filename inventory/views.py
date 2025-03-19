
from django.shortcuts import render, redirect
from .models import Ingredient, MenuItem, RecipeRequirement, Sale
from .forms import IngredientForm, MenuItemForm, SaleForm


def inventory_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'inventory/inventory_list.html', {'ingredients': ingredients})

def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = IngredientForm()
    return render(request, 'inventory/add_ingredient.html', {'form': form})

def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save()

            for requirement in sale.menu_item.reciperequirement_set.all():
                ingredient = requirement.ingredient
                ingredient.available_quantity -= requirement.quantity_required * sale.quantity_sold
                ingredient.save()
            return redirect('inventory_list')
    else:
        form = SaleForm()
    return render(request, 'inventory/add_sale.html', {'form': form})


def sales_report(request):
    sales = Sale.objects.all()
    return render(request, 'inventory/sales_report.html', {'sales': sales})

def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = MenuItemForm()
    return render(request, 'inventory/add_menu_item.html', {'form': form})