from django.urls import path

from catalogue.views import product_list, product_search, user_profile, product_details

urlpatterns = [
    path('product/list/', product_list, name='product-list'),
    path('product/search/', product_search, name='product-search'),
    path('product/profile/', user_profile, name='user-profile'),
    path('product/detail<int:pk>/', product_details, name='product-detail'),
]
