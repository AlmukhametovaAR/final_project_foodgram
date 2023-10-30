from django_filters import rest_framework as filters
from recipes.models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.NumberFilter(method='filter_by_favorite')
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_by_shopping_cart')
    author = filters.NumberFilter(field_name='author__id')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        conjoined=False,
        lookup_expr='in',
    )

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']

    def filter_by_favorite(self, queryset, name, value):
        if self.request and self.request.user.is_authenticated:
            if value:
                return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_by_shopping_cart(self, queryset, name, value):
        if self.request and self.request.user.is_authenticated:
            if value:
                return queryset.filter(inshoppingcart__user=self.request.user)
        return queryset
