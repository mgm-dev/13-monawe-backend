# autopep8: off
from django.views           import View
from pathlib                import Path
from django.http            import JsonResponse
from django.db              import IntegrityError
from django.core            import serializers
from django.core.paginator  import Paginator
from django.core.exceptions import FieldError
from django.http            import JsonResponse

from product.models import Product, ProductImage, ProductOption, ProductTag, Category
from product.models import Subcategory as SC


class All(View):
    def get(self, request):
        try:
            order_by      = request.GET.get('order_by', None)
            page_number   = request.GET.get('page_number', None)
            item_per_page = request.GET.get('item_per_page', None)

            product_list = Product.objects.all().order_by(order_by)
            paginator    = Paginator(product_list, item_per_page)

            data = []

            for product in paginator.get_page(page_number):
                data.append(product.get_info())

            return JsonResponse({ "numPages" : paginator.num_pages, "data" : data }, status=200)

        except ValueError:
            return JsonResponse({ "message" : "VALUE_ERROR"}, status=400)
        except TypeError:
            return JsonResponse({ "message" : "TYPE_ERROR"}, status=400)
        except FieldError:
            return JsonResponse({ "message" : "FIELD_ERROR"}, status=400)


class Category(View):
    def get(self, request, category_id):
        try:
            order_by      = request.GET.get('order_by', None)
            page_number   = request.GET.get('page_number', None)
            item_per_page = request.GET.get('item_per_page', None)
            subcategories = SC.objects.filter(category_id=category_id)

            product_list = Product.objects.filter(subcategory__in=subcategories).order_by(order_by)
            paginator    = Paginator(product_list, item_per_page)

            data = []

            for product in paginator.get_page(page_number):
                data.append(product.get_info())

            return JsonResponse({ "numPages" : paginator.num_pages, "data" : data}, status=200)

        except ValueError:
            return JsonResponse({ "message" : "VALUE_ERROR"}, status=400)
        except TypeError:
            return JsonResponse({ "message" : "TYPE_ERROR"}, status=400)
        except FieldError:
            return JsonResponse({ "message" : "FIELD_ERROR"}, status=400)

class Search(View):
    def get(self,request):
        try:
            search_word = request.GET.get('search_word')

            if len(search_word) == 0 :
                return JsonResponse({"data" : []}, status=200)

            product_list = Product.objects.filter(name__contains=search_word)

            data = []

            for product in product_list:
                data.append(product.get_info())

            return JsonResponse({"data" : data}, status=200)

        except ValueError:
            return JsonResponse({ "message" : "VALUE_ERROR"}, status=400)
        except TypeError:
            return JsonResponse({ "message" : "TYPE_ERROR"}, status=400)
        except FieldError:
            return JsonResponse({ "message" : "FIELD_ERROR"}, status=400)


class Subcategory(View):
    def get(self, request, subcategory_id):
        try:
            order_by      = request.GET.get('order_by', None)
            page_number   = request.GET.get('page_number', None)
            item_per_page = request.GET.get('item_per_page', None)

            product_list = Product.objects.filter(subcategory_id=subcategory_id).order_by(order_by)
            paginator    = Paginator(product_list, item_per_page)

            data = []

            for product in paginator.get_page(page_number):
                data.append(product.get_info())

            return JsonResponse({ "numPages" : paginator.num_pages, "data" : data }, status=200)

        except ValueError:
            return JsonResponse({ "message" : "VALUE_ERROR"}, status=400)
        except TypeError:
            return JsonResponse({ "message" : "TYPE_ERROR"}, status=400)
        except FieldError:
            return JsonResponse({ "message" : "FIELD_ERROR"}, status=400)

class Detail(View):
    def get(self, request, product_id):
        try:
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

        except Product.DoesNotExist:
            return JsonResponse({ "message" : "PRODUCT_DOES_NOT_EXIST"}, status=404)

