from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
from catalogue.models import Product


# Create your views here.


def product_list(requests):
    return HttpResponse('product list')


def product_search(requests):
    """
    in search bar after / we can send queryset wit ? q="word we want to search"
    in title we get q value from front and in products we search in database when
    that products is avalable  or not and inside we check params like is_activate
    and search in title names  ,
    title__icontains it means no diffrent title start with title or contians or
    capital.....
    :param requests:
    :return:
    """
    title = requests.GET.get('q')
    products = Product.objects.filter(
        is_activate=True, title__icontains=title
    )
    context = "\n".join(f"{product.title}--{product.upc}." for product in products)
    return HttpResponse(f"search page:{context}")

@login_required(login_url='/admin/login/')
@require_http_methods(['GET', 'POST'])
def user_profile(requests):
    return HttpResponse(f"hello {requests.user}")

