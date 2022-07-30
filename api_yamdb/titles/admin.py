from django.contrib import admin

from .models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


class CategoriesAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


class GenresAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(Genre, GenresAdmin)
