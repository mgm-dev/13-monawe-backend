from django.shortcuts import render

from product.models import Product, Category
from product.models import Subcategory as SC
from django.views import View
from django.http import JsonResponse


class All(View):
    def get(self, request):
        data = list(Product.objects.all().values())
        return JsonResponse(data, safe=False)


class Category(View):
    def get(self, request, category_id):
        subcategories = SC.objects.filter(
            category_id=category_id)
        data = list(Product.objects.filter(
            subcategory__in=subcategories).values())
        return JsonResponse(data, safe=False)


class Subcategory(View):
    def get(self, request, subcategory_id):
        data = list(Product.objects.filter(
            subcategory_id=subcategory_id).values())
        return JsonResponse(data, safe=False)
