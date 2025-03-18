from django import forms
from .models import Ingredient, MenuItem, Sale

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'price_per_unit', 'available_quantity']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'ingredients']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['menu_item', 'quantity_sold']