import json

from django.http    import JsonResponse
from django.views   import View

from order.models import ProductReview, WishProduct, Order
from user.models import User, Address
from product.models import Product

# Create your views here.

# Review
class ReviewUploadView(View):

    def post(self, request):
        data = json.loads(request.body)
        ProductReview(
            user        = User.objects.get(id=data['user']),
            product     = Product.objects.get(id=data['product']),
            rating      = data['rating'],
            title       = data['title'],
            content     = data['content'],
            created_at  = data['created_at'],
            updated_at  = data['updated_at'],
            image_url   = data['image_url'],
        ).save()
        return JsonResponse(
            {'MESSAGE':'Review uploaded'},
            status = 201
        )
        
class ReviewShowView(View):
    
    def get(self, request):
        data = json.loads(request.body)
        reviews = ProductReview.objects.filter(product_id = data['product_id']).values()
        review_list = []
        for review in reviews:
            review_list.append(review)

        return JsonResponse(
            {'MESSAGE': review_list},
            status = 200
        )

# Wish List
class AddWishView(View):

    def post(self, request):
        data = json.loads(request.body)
        WishProduct(
            user    = User.objects.get(id = data['user']),
            product = Product.objects.get(id = data['product'])
        ).save()
        return JsonResponse(
            {'MESSAGE':'Added to the wishlist'},
            status = 200
        )

class ShowWishView(View):

    def get(self, request):
        data = json.loads(request.body)
        wish_items = WishProduct.objects.filter(user_id = data['user_id']).values()
        item_list = []
        for item in wish_items:
            item_list.append(item)

        return JsonResponse(
            {'MESSAGE': item_list},
            status = 200
        )

# Order




# class PlaceOrderView(View):

#     def post(self, request):
#         data = json.loads(request.body)
#         Order(
#             user = User.objects.get(id=data['user']),
#             address = Address.objects.get(id=data['address']),
#             order_request = data['request'],
#             data = data['date']
#         ).save()
#         return JsonResponse(
#             {'MESSAGE':'Order Success'},
#             status = 200
#         )
