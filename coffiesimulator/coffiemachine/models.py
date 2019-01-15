from django.db import models
from abc import ABC, abstractmethod
from django.http import HttpResponseServerError
from .constants import INGREDIENTS
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
    
    # ingredients = models.ForeignKey(
    #     RecipeIngredientsAmount,
    #     models.DO_NOTHING,
    #     related_name='recipe_ingredient',

    class Meta:
        db_table = 'recipes'
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')

    def __str__(self):
        return self.name




# class Vessel(ABC):
#     def get_amount(self, reagent):
#         try:
#             reagent.objects.get('amount')
#         except models.ObjectDoesNotExist as e:
#             return HttpResponseServerError(f'Cannot get amount of {reagent} now. Error message: {e}')
    

class WaterVessel(object):
    pass


class MilkVessel(object):
    pass

class CoffieVessel(object):
    pass


