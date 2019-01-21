from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Recipe, CoffeeMachine, IngredientManager, Ingredient
from django.core.exceptions import ValidationError


def recipes_list(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'coffeemachine/index.html', context=context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        machine = CoffeeMachine(recipe)

        try:
            your_coffee = machine.make_coffee()
        except ValidationError:
            return HttpResponseRedirect(reverse('ingredients'))

        context = {
            'coffee': your_coffee,
        }
        return render(request, 'coffeemachine/enjoy_your_coffee.html', context=context)
    else:
        context = {
            'recipe': recipe,
        }
        return render(request, 'coffeemachine/recipe_detail.html', context=context)

def ingredients(request):
    ingredients = Ingredient.objects.all()
    if request.method == 'POST':
        for ingredient in ingredients:
            ingredient.fill_ingredient()

    context = {
            'ingredients': ingredients,
        }
    return render(request, 'coffeemachine/ingredients.html', context=context)
