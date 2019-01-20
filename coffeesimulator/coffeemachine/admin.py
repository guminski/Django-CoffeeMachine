from django.contrib import admin
from .models import (
    Ingredient,
    Recipe,
    RecipeRequiredIngredients,
)

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeRequiredIngredients)