from django.contrib import admin
from catalogue.models import Category, Brand, Product, ProductType, ProductAttribute
# Register your models here.


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute


class ProductAdmin(admin.ModelAdmin):
    list_display = ['upc', 'title', 'category', 'brand', 'is_activate']
    list_filter = ['is_activate', 'brand', 'category']
    list_editable = ['is_activate']
    search_fields = ['upc', 'title', 'category__name', 'brand__name']


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product_type', 'title', 'attribute_type']


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    inlines = [ProductAttributeInline]


admin.site.register(Category)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
