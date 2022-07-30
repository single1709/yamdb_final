from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True,
        many=False,
    )
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)

    def validate_year(value):
        if value > datetime.now().year:
            raise ValidationError(
                f'Год {value} больше текущего!',
                params={'value': value},
            )


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        many=False,
        read_only=False,
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        read_only=False,
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)
