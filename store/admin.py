from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'category', 'slug', 'is_available', 'created_at', 'modified_at')
    list_display_links = ('product_name', 'category',)

    # filter_horizontal = ()
    # list_filter = ()

admin.site.register(Product, ProductAdmin)