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
        order_by = request.GET.get('order_by', None)
        products = []

        if order_by:
            for product in Product.objects.all().order_by(order_by):
                products.append(product.get_info())
        else:
            for product in Product.objects.all():
                products.append(product.get_info())

        return JsonResponse({ "data" : products}, status=200)

class Category(View):
    def get(self, request, category_id):
        order_by = request.GET.get('order_by', None)
        subcategories = SC.objects.filter(category_id=category_id)
        products = []

        if order_by:
            for product in Product.objects.filter(subcategory__in=subcategories).order_by(order_by):
                products.append(product.get_info())
        else:
            for product in Product.objects.filter(subcategory__in=subcategories):
                products.append(product.get_info())

        return JsonResponse({ "data" : products}, status=200)

class Subcategory(View):
    def get(self, request, subcategory_id):
        order_by = request.GET.get('order_by', None)
        products = []

        if order_by:
            for product in Product.objects.filter(subcategory_id=subcategory_id).order_by(order_by):
                products.append(product.get_info())
        else:
            for product in Product.objects.filter(subcategory_id=subcategory_id):
                products.append(product.get_info())

        return JsonResponse({ "data" : products}, status=200)

class Detail(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)

        bodyColor = []
        inkColor  = []

        for product_option in ProductOption.objects.filter(product=product):
            body         = {}
            body['name'] = product_option.body_color.name
            body['hex']  = product_option.body_color.hex_code

            ink         = {}
            ink['name'] = product_option.ink_color.name
            ink['hex']  = product_option.ink_color.hex_code

            bodyColor.append(body)
            inkColor.append(ink)

        data = {
            'productInfo': {
                'name'       : product.name,
                'imageUrl'   : [product_image.image_url for product_image in ProductImage.objects.filter(product=product)],
                'bodyColor'  : bodyColor,
                'inkColor'   : inkColor,
                'thickness'  : [product_option.thickness.value for product_option in ProductOption.objects.filter(product=product)],
                'description': product.description,
                'tag'        : [productTag.tag.name for productTag in ProductTag.objects.filter(product=product)],
                'price'      : product.price,
                'options'    : [product_option.body_color.name + "/" + product_option.ink_color.name
                                + "(" + product_option.thickness.value + "mm)"
                                + "(재고:" + str(product_option.stock) + "개)"
                                for product_option in ProductOption.objects.filter(product=product)],
                'stock'      : [product_option.stock for product_option in ProductOption.objects.filter(product=product)]
            }
        }

        return JsonResponse({ "data" : data}, status=200)
