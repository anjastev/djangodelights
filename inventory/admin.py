from django.contrib import admin
from .models import Ingredient, RecipeRequirement

admin.site.register(Ingredient)
admin.site.register(RecipeRequirement)
