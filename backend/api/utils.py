from django.shortcuts import get_object_or_404
from recipes.models import IngredientRecipe, Recipe, TagRecipe
from rest_framework import status
from rest_framework.response import Response


def add_delete_recipe(choice_model, choice_serializer, request, recipe_id):
    """
    @action decorator function to add or remove recipe from favorites
    and shopping cart.
    """
    chosen_recipe = get_object_or_404(Recipe, pk=recipe_id)
    user = request.user

    if request.method == 'POST':

        already_added = choice_model.objects.filter(
            user=user,
            recipe=chosen_recipe
        ).exists()
        if already_added:
            return Response(
                {'errors': 'You have already added this recipe.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        added = choice_model.objects.create(
            user=user,
            recipe=chosen_recipe
        )
        serializer = choice_serializer(chosen_recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':

        added = choice_model.objects.filter(
            user=user,
            recipe=chosen_recipe
        ).first()
        if not added:
            return Response(
                {'errors': 'You did not add this recipe.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        added.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def is_added(self, obj, choice_model):
    """
    Function to check if a recipe is in Favorite or InShoppingCart.
    """
    user = self.context['request'].user
    is_added = choice_model.objects.filter(
        user=user, recipe=obj
    ).exists()
    return is_added


def tag_recipe_save(tags, recipe):
    """
    Function to save tags in recipe.
    Function is used in create/update functions of RecipeSerializer.
    """
    tag_recipes = []
    for tag in tags:
        tag_recipe = TagRecipe(recipe=recipe, tag=tag)
        tag_recipes.append(tag_recipe)
    TagRecipe.objects.bulk_create(tag_recipes)


def ingredient_recipe_save(ingredients_data, recipe):
    """
    Function to save ingredients data in recipe.
    Function is used in create/update functions of RecipeSerializer.
    """
    ingredient_recipes = []
    for ingredient_data in ingredients_data:
        ingredient_recipe = IngredientRecipe(
            recipe=recipe, **ingredient_data)
        ingredient_recipes.append(ingredient_recipe)
    IngredientRecipe.objects.bulk_create(ingredient_recipes)
