from django.db import models
from abc import ABC, abstractmethod
from django.http import HttpResponseServerError
from .constants import INGREDIENTS, MAX_TANK_CAPACITY
from django.utils.translation import ugettext_lazy as _

class Ingredient(models.Model):
    """
    Ingredient model
    """
    name = models.CharField(
        max_length=8,
        choices=INGREDIENTS,
        help_text=_("Ingredient name"),
    )
    amount_left = models.FloatField(
        default=0,
    )

    def pop_ingredient(self, amount):
        self.amount_left -= amount
        self.save()
        return amount
    
    def fill_ingredient(self):
        self.amount_left = MAX_TANK_CAPACITY

    class Meta:
        db_table = 'ingredients'
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

    def __str__(self):
        return self.name


class RecipeIngredientsAmount(models.Model):
    """
    Recipe ingredient and their amounts
    """
    ingredient = models.ForeignKey(
        'Ingredient',
        models.SET_NULL,
        null=True,
        related_name='ingredient_amount',
    )
    recipe = models.ForeignKey(
        'Recipe',
        models.SET_NULL,
        null=True,
        blank=True,
        related_name='ingredient_amount',
    )
    required_amount = models.FloatField(
        help_text=_('Recipe ingredient required amount'),
    )

    class Meta:
        db_table = 'recipeingredients'
        verbose_name = _('recipe ingredient')
        verbose_name_plural = _('recipe ingredients')
        unique_together = (('recipe', 'ingredient'),)

    def __str__(self):
        return str(self.recipe) + ' - ' + self.ingredient.name + ' - ' + str(self.required_amount)


class Recipe(models.Model):
    """
    Recipe model which depends on Ingredient and amount
    """
    name = models.CharField(
        max_length=64,
        help_text=_('Recipe name'),
    )
    description = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text=_('Recipe description'),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredientsAmount',
        help_text=_('user district role'),
    )
    #TODO ADD unique together milk coffie and water
 
    class Meta:
        db_table = 'recipes'
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')

    def __str__(self):
        return self.name


class Tank(ABC):
    name = NotImplemented
    pump_state = False
    ingredient = NotImplemented

    @abstractmethod
    def get_ingredients(self):
        pass

    def _enable_tool(self, tool):
        self.tool = True

    def _distable_tool(self, tool):
        self.tool = False

    # def pop_ingredient(self, amount, ingredient):
    #     self.recipe.ingredient.pop_ingredient(amount)
    #     return amount


class WaterTank(Tank):
    def __init__(self, ingredient):
        self.name = 'Water Tank'
        self.ingredient_name='WATER'
        self.water = self.ingredient.objects.get(name=self.ingredient_name)
        self.heater_state = False

    def get_ingredients(self, amount):
        return self.water.pop_ingredient(amount)

    def fill_ingredient(self):
        return self.water.fill_ingredient()

class MilkTank(Tank):
    name = 'Milk Tank'


class CoffeeTank(object):
    grinder_state = False

    def grind(self):
        self.grinder_state = True

    def stop_grinding(self):
        self.grinder_state = False


# class TankManager(object):
#     def __init__(self):
#         self.milk=MilkTank
#         self.coffee=CoffeeTank
#         self.water=WaterTank
#         self.ingredient=Ingredient


class RecipeManager(Recipe):

    def pop_ingredient(self, amount, ingredient_name):
        self.ingredients.filter(ingredient_name).pop_ingredient(amount)
        return self
    def set_recipe(self, pk):
        self.recipe = recipe.objects.get(pk=pk)

    class Meta:
        abstract = True
        managed = False


class CoffeeMachine(object):
    def __init__(self, tank_manager, recipe_manager):
        self.tanks = tank_manager
        self.recipes = recipe_manager

        