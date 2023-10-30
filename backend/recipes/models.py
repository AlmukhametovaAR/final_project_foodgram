from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'ingredient name',
        max_length=200
    )
    measurement_unit = models.CharField(
        'unit of ingredient measurement',
        max_length=200
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'tag name',
        unique=True,
        max_length=100
    )
    color = ColorField(
        'HEX color',
        unique=True
    )
    slug = models.SlugField(
        'unique URL fragment',
        unique=True,
        max_length=200
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        'recipe name',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        verbose_name='recipe author',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    pub_date = models.DateTimeField(
        'date the recipe was added',
        auto_now_add=True,
        db_index=True
    )
    image = models.ImageField(
        'finished dish photo',
        upload_to='recipes/'
    )
    text = models.TextField(
        'recipe description'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'cooking time in minutes',
        validators=[MinValueValidator(
            1, 'Cooking time cannot be less than 1 minute'
        )]
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'

    def __str__(self):
        return f'{self.name} {self.author}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        'ingredient amount in recipe',
        validators=[MinValueValidator(
            1, 'Ingredient amount cannot be less than 1'
        )]
    )

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='favorite_unique_relationships',
                fields=['user', 'recipe'],
            )
        ]


class InShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} {self.recipe}'
