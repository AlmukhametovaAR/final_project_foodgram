import webcolors
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                            InShoppingCart, Recipe, Tag)
from rest_framework import serializers
from users.serializers import UserListSerializer

from .utils import ingredient_recipe_save, is_added, tag_recipe_save


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError(
                'There is no name for this color.'
            )
        return data


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient_id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    ingredients = IngredientRecipeSerializer(
        source='ingredientrecipe_set', many=True)
    author = UserListSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tags_id = representation['tags']
        tags = Tag.objects.filter(id__in=tags_id)
        serializer = TagSerializer(tags, many=True)
        representation['tags'] = serializer.data
        return representation

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredientrecipe_set')
        recipe = Recipe.objects.create(**validated_data)
        tag_recipe_save(tags, recipe)
        ingredient_recipe_save(ingredients_data, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredientrecipe_set', [])
        tags = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)

        instance.tags.clear()
        tag_recipe_save(tags, instance)

        instance.ingredientrecipe_set.all().delete()
        ingredient_recipe_save(ingredients_data, instance)

        return instance

    def get_is_favorited(self, obj):
        return is_added(self, obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return is_added(self, obj, InShoppingCart)
