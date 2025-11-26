from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('delete_product/<int:product_id>/<int:cart_item_id>/', views.delete_cart_item, name='delete_product'),
    path('decrease_product/<int:product_id>/<int:cart_item_id>/', views.decrease_item, name='decrease_product'),
    # path('<slug:category_slug>/', views.store, name='products_by_category'),
    # path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]
