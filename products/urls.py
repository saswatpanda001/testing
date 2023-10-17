from products.models import Product_Model
from django.urls import path
from products import views

app_name = "products"

urlpatterns = [
    path("create", views.create_product.as_view(), name="create"),
    path("list", views.product_view, name="home"),
    path("products/", views.prod_list, name="all_pr"),
    path("update/<int:pk>", views.product_updateview.as_view(), name="update"),
    path("delete/<int:pk>", views.product_deleteview.as_view(), name="delete"),
    path("cart/check", views.confirm_orders, name="confirm_order"),
    path("products/<int:pk>", views.products_details, name="pr_details"),
    path("cart", views.cart_view, name="cart"),
    path("cart/delete/<int:pk>", views.cart_deleteview.as_view(), name="del_cart"),
    path("cart/confirm", views.confirm, name="confirm"),
    path("orders/", views.orders, name="orders"),
    path("orders/<str:pk>", views.ord_details, name="ord_details"),
    path("sales/", views.sales, name="sales"),
    path("sales/<str:pk>", views.sale_details, name="sale_details"),
    path("wishlist", views.wishlist_data, name="wishlist")


]
