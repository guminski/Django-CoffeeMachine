from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Recipe, CoffeeMachine, IngredientManager


def recipes_list(request):
    recipes = Recipe.objects.all()

    context = {
        'recipes': recipes,
    }
    return render(request, 'coffeemachine/index.html', context=context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        machine = CoffeeMachine(IngredientManager, recipe)
        result = machine.make_coffee()
        return HttpResponse(f"POST dla {recipe_id}: {result}")
    else:
        context = {
            'recipe': recipe,
        }
        return render(request, 'coffeemachine/recipe_detail.html', context=context)