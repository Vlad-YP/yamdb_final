from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'score', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date', 'score', 'title')
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment)
admin.site.register(GenreTitle)
