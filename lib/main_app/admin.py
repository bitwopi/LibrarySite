from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Author, Book, Instance, Rent, Genre


# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'second_name', 'patronymic', 'birth_date', 'description', 'get_html_photo')
    search_fields = ('second_name', 'first_name')
    list_editable = ('first_name', 'second_name', 'patronymic', 'birth_date', 'description',)
    fields = ('first_name', 'second_name', 'patronymic', 'birth_date', 'description', 'photo', 'get_html_photo')
    prepopulated_fields = {'slug': ("second_name", "first_name")}

    def get_html_photo(self, obj):
        return mark_safe(f"<img src='{obj.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    prepopulated_fields = {'slug': ("name",)}


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'pages', 'cost', 'author', 'get_html_cover', 'get_genres')
    search_fields = ('name',)
    list_editable = ('name', 'description', 'pages', 'cost', 'author',)
    list_display_links = ('id', 'get_genres')
    prepopulated_fields = {'slug': ("name",)}
    fields = ('name', 'slug', 'description', 'pages', 'cost', 'author', 'cover', 'get_html_cover', 'genres')
    readonly_fields = ('get_html_cover',)

    def get_html_cover(self, obj):
        return mark_safe(f"<img src='{obj.cover.url}' width=50>")

    get_html_cover.short_description = "Миниатюра"


class InstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'in_stock',)
    search_fields = ('book', 'in_stock')
    list_editable = ('in_stock',)


class RentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'instance_id', 'start_date', 'end_date', 'actual_end_date',)
    search_fields = ('user_email', 'instance_id')
    list_editable = ('user_email', 'instance_id', 'actual_end_date',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Rent, RentAdmin)
