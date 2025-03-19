from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=2)
    available_quantity = models.FloatField()

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=[
        ('appetizer', 'Appetizer'),
        ('main_course', 'Main Course'),
        ('dessert', 'Dessert'),
    ], default='main_course')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.category}"


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_required = models.FloatField()

    def __str__(self):
        return f"{self.menu_item.name} needs {self.quantity_required} {self.ingredient.name}"


class Sale(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.menu_item.price * self.quantity_sold

    def __str__(self):
        return f"Sold {self.quantity_sold} of {self.menu_item.name} on {self.timestamp}"
