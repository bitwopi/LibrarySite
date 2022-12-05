from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'second_name', 'patronymic')}),
        (_('Permissions'), {'fields': ('is_superuser', 'group',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'second_name', 'is_staff')
    list_filter = ('is_superuser', 'group')
    readonly_fields = ('is_staff', 'date_joined')
    search_fields = ('first_name', 'second_name', 'email')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
