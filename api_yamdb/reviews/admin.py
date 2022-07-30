from django.contrib import admin

from .models import Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)


class CommentAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


admin.site.register(Comment, CommentAdmin)
