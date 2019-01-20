from django.db import models
from abc import ABC, abstractmethod
from django.http import HttpResponseServerError
from .constants import INGREDIENTS, MAX_TANK_CAPACITY
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class Ingredient(models.Model):
    """
    Ingredient model
    """
    name = models.CharField(
        max_length=8,
        choices=INGREDIENTS,
        help_text=_('Ingredient name'),
    )
    amount_left = models.FloatField(
        default=0,
    )

    def clean(self):
        if self.amount_left < 0 or self.amount_left > MAX_TANK_CAPACITY:
            raise ValidationError(f'Ingredient amount_left have to be in range 0 - {MAX_TANK_CAPACITY}')

    def pop_ingredient(self, amount):
        self.amount_left -= amount
        self.clean()
        self.save()
        return amount

    def fill_ingredient(self):
        self.amount_left = MAX_TANK_CAPACITY
        self.save()
        return self.amount_left

    class Meta:
        db_table = 'ingredients'
        ordering = ['name']
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

    def __str__(self):
        return self.name


class RecipeRequiredIngredients(models.Model):
    """
    Recipe ingredient and their amounts
    """
    ingredient = models.ForeignKey(
        'Ingredient',
        models.CASCADE,
        related_name='ingredient_amount',
    )
    recipe = models.ForeignKey(
        'Recipe',
        models.CASCADE,
        related_name='ingredient_amount',
    )
    required_amount = models.FloatField(
        help_text=_('Recipe ingredient required amount'),
    )

    class Meta:
        db_table = 'recipeingredients'
        ordering = ['recipe']
        verbose_name = _('recipe ingredient')
        verbose_name_plural = _('recipe ingredients')
        unique_together = (('recipe', 'ingredient'),)

    def __str__(self):
        return str(self.recipe) + ' - ' + self.ingredient.name + ' - ' + str(self.required_amount)


class Recipe(models.Model):
    """
    Recipe model - depends on Ingredient and ingredients amount
    """
    name = models.CharField(
        max_length=64,
        help_text=_('Recipe name'),
        unique=True,
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
        through='RecipeRequiredIngredients',
        help_text=_('Ingredients and their amounts'),
    )
 
    class Meta:
        db_table = 'recipes'
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')

    def __str__(self):
        return self.name


class IngredientManager(object):
    """
    Managing amounts of ingredients
    """
    @classmethod
    def pop_ingredient(self, cls, amount):
        cls.pop_ingredient(amount)
        return cls

    @classmethod
    def fill_ingredient(self, cls):
        cls.fill_ingredient
        return cls

class Tank(ABC):
    name = NotImplemented
    ingredient_name = NotImplemented\


class Fluid(ABC):
    def enable_heater(self):
        self._heater_state = True

    def disable_heater(self):
        self._heater_state = False

    def enable_pump(self):
        self._pump_state = True

    def disable_pump(self):
        self._pump_state = False


class WaterTank(Tank, Fluid):
    def __init__(self):
        self.name = 'Water Tank'
        self.ingredient_name = 'WATER'
        self._heater_state = False
        self._pump_state = False


class MilkTank(Tank, Fluid):
    def __init__(self):
        self.name = 'Milk Tank'
        self.ingredient_name = 'MILK'
        self._heater_state = False
        self._pump_state = False


class CoffeeTank(Tank):
    def __init__(self):
        self.name = 'Coffee Tank'
        self.ingredient_name = 'COFFEE'
        self._grinder_state = False

    def grind(self):
        self._grinder_state = True

    def stop_grinding(self):
        self._grinder_state = False


class TankManager(object):
    def __init__(self, water_tank, milk_tank, coffee_tank):
        self.milk_tank = milk_tank
        self.coffee_tank = coffee_tank
        self.water_tank = water_tank


class CoffeeMachine(object):
    def __init__(self, ingredient_manager, recipe, tank_manager):
        self.ingredient_manager = ingredient_manager
        self.recipe = recipe
        self.tank_manager = tank_manager

    def get_ingredient_req_amounts(self):
        req_ingredients = self.recipe.ingredient_amount.iterator()
        return req_ingredients

    def make_coffee(self):
        req_ingredients = self.get_ingredient_req_amounts()
        
        for e in req_ingredients:

            self.ingredient_manager.pop_ingredient(e.ingredient, e.required_amount)

        return self.recipe.name




        