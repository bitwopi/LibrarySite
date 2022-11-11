from django.contrib import admin
from .models import Author, Book, Instance, Rent
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'second_name', 'patronymic', 'birth_date', 'description',)
    search_fields = ('second_name', 'first_name')
    list_editable = ('first_name', 'second_name', 'patronymic', 'birth_date', 'description',)
    prepopulated_fields = {'slug': ("second_name", "first_name")}


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'pages', 'cost', 'author',)
    search_fields = ('name',)
    list_editable = ('name', 'description', 'pages', 'cost', 'author',)
    prepopulated_fields = {'slug': ("name",)}


class InstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'in_stock',)
    search_fields = ('book', 'in_stock')
    list_editable = ('in_stock',)


class RentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'instance_id', 'start_date', 'end_date', 'actual_end_date', 'cost',)
    search_fields = ('user_email', 'instance_id')
    list_editable = ('user_email', 'instance_id', 'actual_end_date', 'cost',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Rent, RentAdmin)
