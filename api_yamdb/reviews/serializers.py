from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Comment, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        model = Review

    def validate(self, data):
        title_id = (
            self
            .context['request']
            .parser_context['kwargs']
            .get('title_id')
        )
        user = self.context['request'].user
        title = get_object_or_404(Title, id=title_id)
        if (self.context['request'].method == 'POST') and (
            Review.objects.filter(author=user, title=title).exists()
        ):
            response = {
                'review': 'Отзыв уже есть.'
            }
            raise serializers.ValidationError(response)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        exclude = ('review',)
        model = Comment
        read_only_fields = ('review',)
