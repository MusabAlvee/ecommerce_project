from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    list_display_links = ('username', 'email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, MyUserAdmin)