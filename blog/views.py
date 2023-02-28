from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
from catalogue.models import Product
# Create your views here.


def post_list(request, year=None, month=None):
    if month is not None:
        return HttpResponse(f"post list archive for {year} and {month}")
    if year is not None:
        return HttpResponse(f"post list archive for {year}")
    return HttpResponse('IS NOT YEAR')


def categories_list(requests):
    return HttpResponse('category list page')
