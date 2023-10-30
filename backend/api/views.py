from common.serializers import RecipeMiniSerializer
from django.db.models import Sum
from django.http import HttpResponse
from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                            InShoppingCart, Recipe, Tag)
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action

from .filters import RecipeFilter
from .permissions import AuthorOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from .utils import add_delete_recipe


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    filterset_class = RecipeFilter
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        return RecipeFilter(
            self.request.GET,
            queryset=Recipe.objects.all().distinct(),
            request=self.request
        ).qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        super().perform_create(serializer)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        return add_delete_recipe(Favorite, RecipeMiniSerializer, request, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        return add_delete_recipe(
            InShoppingCart, RecipeMiniSerializer, request, pk)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated],
            url_path='download_shopping_cart')
    def download_shopping_cart(self, request):

        cart_recipes = InShoppingCart.objects.filter(
            user=request.user).values_list('recipe', flat=True)
        ingredients = IngredientRecipe.objects.filter(
            recipe__in=cart_recipes
        ).values(
            "ingredient__name"
        ).annotate(
            ingredient_amount=Sum("amount")
        )

        ingredient_name_unit = {}
        ingredient_units = Ingredient.objects.filter(
            ingredientrecipe__recipe__in=cart_recipes,
            name__in=[
                ingredient['ingredient__name'] for ingredient in ingredients
            ]
        ).values("name", "measurement_unit")

        for ingredient_unit in ingredient_units:
            ingredient_name_unit[
                ingredient_unit['name']] = ingredient_unit['measurement_unit']

        shopping_cart = []

        for ingredient in ingredients:
            ingredient_name = ingredient['ingredient__name']
            ingredient_unit = ingredient_name_unit.get(ingredient_name)
            shopping_cart.append(f'{ingredient_name} - '
                                 f'{ingredient["ingredient_amount"]} '
                                 f'{ingredient_unit}')

        shopping_cart_text = '\n'.join(shopping_cart)

        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'inline; filename=shopping_cart.txt'
        response.write(shopping_cart_text)
        return response
