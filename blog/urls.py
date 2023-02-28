from django.urls import path
from blog.views import categories_list, post_list

urlpatterns = [
    path('list/category_list', categories_list),
    path('list/post_list', post_list),
]
