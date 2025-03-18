
from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=2)
    available_quantity = models.IntegerField()

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeRequirement')

    def __str__(self):
        return self.name

class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_required = models.IntegerField()

    def __str__(self):
        return f"{self.menu_item.name} requires {self.quantity_required} of {self.ingredient.name}"

class Sale(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    date_sold = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Sale of {self.menu_item.name} - {self.quantity_sold} sold"
