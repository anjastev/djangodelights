from django import forms
from .models import Ingredient, MenuItem, Sale, Order, OrderItem, Employee, Location


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'price_per_unit', 'available_quantity', 'status']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'price']


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['menu_item', 'quantity_sold']

    def clean_quantity_sold(self):
        quantity = self.cleaned_data['quantity_sold']
        menu_item = self.cleaned_data.get('menu_item')

        if menu_item:
            required_ingredients = menu_item.reciperequirement_set.all()
            for req in required_ingredients:
                if req.ingredient.available_quantity < (req.quantity_required * quantity):
                    raise forms.ValidationError(f"Not enough {req.ingredient.name} in stock!")

        return quantity

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'order_date']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'role', 'location']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'phone_number']