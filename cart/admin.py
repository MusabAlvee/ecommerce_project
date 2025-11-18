from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

# class MyUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active', 'created_at')
#     list_display_links = ('username', 'email',)

#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

admin.site.register(Cart)
admin.site.register(CartItem)