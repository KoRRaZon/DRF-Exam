from django.urls import path

from apps.profiles.views import OrderView, OrderItemsView
from apps.shop.views import CategoriesView, ProductsView, ProductView, ProductsByCategoryView, ProductsBySellerView, \
    CheckoutView, CartView

urlpatterns = [
    path("categories/", CategoriesView.as_view()),
    path("categories/<slug:slug>/", ProductsByCategoryView.as_view()),
    path("sellers/<slug:slug>/", ProductsBySellerView.as_view()),
    path("products/", ProductsView.as_view()),
    path("products/<slug:slug>/", ProductView.as_view()),
    path("cart/", CartView.as_view()),
    path("checkout/", CheckoutView.as_view()),
    path("orders/", OrderView.as_view()),
    path("orders/<str:tx_ref>/", OrderItemsView.as_view()),
]