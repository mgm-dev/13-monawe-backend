# autopep8: off
import json

from django.views           import View
from pathlib                import Path
from django.http            import JsonResponse
from django.db              import IntegrityError
from django.core            import serializers
from django.core.exceptions import FieldError
from django.http            import JsonResponse
from django.utils           import timezone

from product.models import Product, ProductImage, ProductOption, ProductTag, Subcategory, Category
from user.models    import User

class ProductList(View):
    def get(self, request):
        try:
            search = request.GET.get('search', None)

            if search:
                if len(search) == 0 :
                    return JsonResponse({"data" : []}, status=200)

                product_list = Product.objects.filter(name__contains=search)
                data = [product.get_info() for product in product_list]

                return JsonResponse({"data" : data}, status=200)

            order_by       = request.GET.get('order_by', None)
            page_number    = int(request.GET.get('page_number', None))
            item_per_page  = int(request.GET.get('item_per_page', None))
            category_id    = request.GET.get('category', None)
            subcategory_id = request.GET.get('subcategory', None)
            offset         = (page_number - 1) * item_per_page

            if subcategory_id:
                filter_condition = {'subcategory_id' : subcategory_id}
            elif category_id:
                subcategories = Subcategory.objects.filter(category_id=category_id)
                filter_condition = {'subcategory__in' : subcategories}
            else:
                filter_condition = {}

            product_count = Product.objects.filter(**filter_condition).count()
            product_list  = Product.objects.filter(**filter_condition).order_by(order_by)[offset:offset+item_per_page]
            num_pages = product_count // item_per_page if product_count % item_per_page == 0 else product_count // item_per_page + 1;

            data = [product.get_info() for product in product_list]

            return JsonResponse({ "num_pages" : num_pages, "num_products" : product_count, "data" : data}, status=200)

        except ValueError:
            return JsonResponse({ "message" : "VALUE_ERROR"}, status=400)
        except TypeError:
            return JsonResponse({ "message" : "TYPE_ERROR"}, status=400)
        except FieldError:
            return JsonResponse({ "message" : "FIELD_ERROR"}, status=400)

class Detail(View):
    def get(self, request, product_id):
        try:
            product             = Product.objects.prefetch_related('productimage_set', 'productoption_set', 'producttag_set').get(id=product_id)
            product_image_list  = product.productimage_set.all()
            product_option_list = product.productoption_set.all()
            product_tag_list    = product.producttag_set.all()

            bodyColor = [
                {
                    'name' : product_option.body_color.name,
                    'hex'  : product_option.body_color.hex_code
                } for product_option in product_option_list
                ]
            inkColor  = [
                {
                    'name' : product_option.ink_color.name,
                    'hex'  : product_option.ink_color.hex_code
                } for product_option in product_option_list
            ]
            options   = [
                {   
                    'id'    : product_option.id,
                    'name'  : product_option.body_color.name + "/" 
                        + product_option.ink_color.name 
                        + "(" + product_option.thickness.value + "mm)" 
                        + "(재고" + str(product_option.stock) + "개)",
                    'price' : product.price + product_option.plus_price
                } for product_option in product_option_list
            ]

            data = {
                'product_info': {
                    'id'         : product.id,
                    'name'       : product.name,
                    'image_url'  : [product_image.image_url for product_image in product_image_list],
                    'body_color' : bodyColor,
                    'ink_color'  : inkColor,
                    'thickness'  : [product_option.thickness.value for product_option in product_option_list],
                    'description': product.description,
                    'tag'        : [product_tag.tag.name for product_tag in product_tag_list],
                    'price'      : product.price,
                    'options'    : options,
                    'stock'      : [product_option.stock for product_option in product_option_list]
                }
            }

            return JsonResponse({ "data" : data}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({ "message" : "PRODUCT_DOES_NOT_EXIST"}, status=404)
