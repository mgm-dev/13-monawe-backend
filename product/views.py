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

from product.models import Product, ProductImage, ProductOption, ProductTag, Subcategory, Category, ProductReview
from user.models    import User

class ProductList(View):
    def get(self, request):
        try:
            order_by       = request.GET.get('order_by', None)
            page_number    = int(request.GET.get('page_number', None))
            item_per_page  = int(request.GET.get('item_per_page', None))
            category_id    = request.GET.get('category', None)
            subcategory_id = request.GET.get('subcategory', None)
            offset         = (page_number - 1) * item_per_page

            if subcategory_id:
                product_count = Product.objects.filter(subcategory_id=subcategory_id).count()
                num_pages     = product_count // item_per_page if product_count % item_per_page == 0 else product_count // item_per_page + 1;
                product_list  = Product.objects.filter(subcategory_id=subcategory_id).order_by(order_by)[offset:offset+item_per_page]
            elif category_id:
                subcategories = Subcategory.objects.filter(category_id=category_id)
                product_count = Product.objects.filter(subcategory__in=subcategories).count()
                num_pages     = product_count // item_per_page if product_count % item_per_page == 0 else product_count // item_per_page + 1;
                product_list  = Product.objects.filter(subcategory__in=subcategories).order_by(order_by)[offset:offset+item_per_page]
            else:
                product_count = Product.objects.all().count()
                num_pages     = product_count // item_per_page if product_count % item_per_page == 0 else product_count // item_per_page + 1;
                product_list  = Product.objects.all().order_by(order_by)[offset:offset+item_per_page]

            data = [product.get_info() for product in product_list]

            return JsonResponse({ "numPages" : num_pages, "data" : data}, status=200)

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

class Detail(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            bodyColor = []
            inkColor  = []
            options   = []

            for product_option in ProductOption.objects.filter(product=product):
                body         = {}
                body['name'] = product_option.body_color.name
                body['hex']  = product_option.body_color.hex_code

                ink         = {}
                ink['name'] = product_option.ink_color.name
                ink['hex']  = product_option.ink_color.hex_code

                option = {}
                option['name'] = body['name'] + "/" + ink['name'] + "(" + product_option.thickness.value + "mm)" + "(재고" + str(product_option.stock) + "개)"
                option['price'] = product.price + product_option.plus_price

                bodyColor.append(body)
                inkColor.append(ink)
                options.append(option)

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
                    'options'    : options,
                    'stock'      : [product_option.stock for product_option in ProductOption.objects.filter(product=product)]
                }
            }

            return JsonResponse({ "data" : data}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({ "message" : "PRODUCT_DOES_NOT_EXIST"}, status=404)

class Review(View):
    def get(self, request):
        product_id = request.GET.get('product_id', None)
        user_id    = request.GET.get('user_id', None)
        review_id  = request.GET.get('review_id', None)

        if product_id:
            review_data = ProductReview.objects.filter(product_id = product_id).values()
            review_list = [review for review in review_data]
        elif user_id:
            review_data = ProductReview.objects.filter(user_id = user_id).values()
            review_list = [review for review in review_data]
        elif review_id:
            review_data = ProductReview.objects.filter(id = review_id).values()
            review_list = [review for review in review_data]
            if len(review_list) == 0:
                return JsonResponse({'MESSAGE': 'REVIEW_DOES_NOT_EXIST'}, status = 404) 

        return JsonResponse({'REVIEWS': review_list}, status = 200)

    def post(self, request):
        data            = json.loads(request.body)
        target_product  = Product.objects.get(id = data['product_id'])

        if ProductReview.objects.filter(product = data['product_id'], user = data['user_id']).exists():
            return JsonResponse({'MESSAGE': 'ALREADY_WROTE_REVIEW'}, status = 400)
        else:
            ProductReview(
                user      = User.objects.get(id = data['user_id']),
                product   = target_product,
                rating    = data['rating'],
                title     = data['title'],
                content   = data['content'],
                image_url = data['image_url'],
            ).save()

            return JsonResponse({'MESSAGE':'REVIEW_UPLOADED'}, status = 201)

    def patch(self, request):
        data           = json.loads(request.body)
        target_review  = ProductReview.objects.get(id = data['review_id'])

        if not ProductReview.objects.filter(id = target_review.id).exists():
            return JsonResponse({'MESSAGE': 'REVIEW_DOES_NOT_EXIST'}, status = 404)
        else:
            ProductReview.objects.filter(id = target_review.id).update(
                rating      = data['rating'],
                title       = data['title'],
                content     = data['content'],
                image_url   = data['image_url'],
                updated_at  = timezone.now(),
            )
            return JsonResponse({'MESSAGE':'REVIEW_UPDATED'}, status = 201)

    def delete(self, request):
        data           = json.loads(request.body)
        target_review  = ProductReview.objects.get(id = data['review_id'])

        if not ProductReview.objects.filter(id = target_review.id).exists():
            return JsonResponse({'MESSAGE': 'REVIEW_DOES_NOT_EXIST'}, status = 404)
        else:
            ProductReview.objects.filter(id = target_review.id).delete()
            return JsonResponse({'MESSAGE': 'REVIEW_DELETED'}, status = 200)
