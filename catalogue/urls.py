from django.urls import path

from catalogue.views import product_list, product_search

urlpatterns = [
    path('product/list/', product_list, name='product-list'),
    path('product/search/', product_search, name='product-search'),
]