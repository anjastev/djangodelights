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

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_process', 'In Process'),
        ('completed', 'Completed'),
    ]
    customer = models.CharField(max_length=100)
    order_items = models.ManyToManyField(MenuItem, through='OrderItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

    def calculate_total(self):
        self.total_price = sum([item.menu_item.price * item.quantity for item in self.orderitem_set.all()])
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} - {self.quantity}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('chef', 'Chef'), ('waiter', 'Waiter')])
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} ({self.role})'


class InventoryHistory(models.Model):
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    change_date = models.DateTimeField(default=timezone.now)
    change_amount = models.IntegerField()
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.ingredient.name} - {self.change_amount}'