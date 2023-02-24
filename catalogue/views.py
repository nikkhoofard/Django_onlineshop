from django.shortcuts import render, HttpResponse

from catalogue.models import Product


# Create your views here.


def product_list(requests):
    return HttpResponse('product list')


def product_search(requests):
    title = requests.GET.get('q')
    products = Product.objects.filter(
        is_activate=True, title__icontains=title
    )
    context = "\n".join(f"{product.title}--{product.upc}." for product in products)
    return HttpResponse(f"search page:{context}")


