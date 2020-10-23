# autopep8: off
from django.views import View
from pathlib      import Path
from django.http  import JsonResponse
from django.db    import IntegrityError
from django.core  import serializers

from product.models import Product, ProductImage, ProductOption, ProductTag, Category
from product.models import Subcategory as SC
from django.views   import View
from django.http    import JsonResponse


class All(View):
    def get(self, request):
        products = []
        for product in Product.objects.all():
            data = {
                'id': product.id,
                'name': product.name,
                'subcategory_name': SC.objects.get(id=product.subcategory_id).name,
                'created_at': product.created_at,
                'company': product.company,
                'description': product.description,
                'sales_amount': product.sales_amount,
            }

            try:
                data['image_url'] = product.productimage_set.all()[0].image_url
            except IndexError:
                data['image_url'] = ""

            products.append(data)

        return JsonResponse(products, safe=False)


class Category(View):
    def get(self, request, category_id):
        subcategories = SC.objects.filter(category_id=category_id)
        products = []
        for product in Product.objects.filter(subcategory__in=subcategories):
            data = {
                'id': product.id,
                'name': product.name,
                'subcategory_name': SC.objects.get(id=product.subcategory_id).name,
                'created_at': product.created_at,
                'company': product.company,
                'description': product.description,
                'sales_amount': product.sales_amount,
            }

            try:
                data['image_url'] = product.productimage_set.all()[0].image_url
            except IndexError:
                data['image_url'] = ""

            products.append(data)

        return JsonResponse(products, safe=False)



class Subcategory(View):
    def get(self, request, subcategory_id):
        products = []
        for product in Product.objects.filter(subcategory_id=subcategory_id):
            data = {
                'id': product.id,
                'name': product.name,
                'subcategory_name': SC.objects.get(id=product.subcategory_id).name,
                'created_at': product.created_at,
                'company': product.company,
                'description': product.description,
                'sales_amount': product.sales_amount,
            }

            try:
                data['image_url'] = product.productimage_set.all()[0].image_url
            except IndexError:
                data['image_url'] = ""

            products.append(data)

        return JsonResponse(products, safe=False)

