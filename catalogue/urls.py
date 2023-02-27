from django.urls import path

from catalogue.views import product_list, product_search, user_profile

urlpatterns = [
    path('product/list/', product_list, name='product-list'),
    path('product/search/', product_search, name='product-search'),
    path('product/profile/', user_profile, name='user-profile'),
]