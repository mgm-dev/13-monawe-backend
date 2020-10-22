import json

from django.http    import JsonResponse
from django.views   import View

from order.models import ProductReview, WishProduct, Order
from user.models import User, Address
from product.models import Product

# Create your views here.

# Order

class PlaceOrderView(View):

    def post(self, request):
        data = json.loads(request.body)
        ordering_user = User.objects.get(id = data['user_id'])
        deliever_address = Address.objects.get(id = data['address_id'])

        Order(
            user = ordering_user,
            address = deliever_address,
            order_request = data['request'],
            date = data['date']
        ).save()

        return JsonResponse(
            {'MESSAGE':'Order Success'},
            status = 200
        )

# Review
class ReviewUploadView(View):

    def post(self, request):
        data            = json.loads(request.body)
        target_product  = Product.objects.get(id = data['product_id'])

        ProductReview(
            user        = User.objects.get(id = data['user_id']),
            product     = target_product,
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
        review_list = [review for review in reviews]

        return JsonResponse(
            {'REVIEWS': review_list},
            status = 200
        )

# Wish List
class AddWishView(View):

    def post(self, request):
        data            = json.loads(request.body)
        wishing_user    = User.objects.get(id = data['user_id'])
        wished_product  = Product.objects.get(id = data['product_id'])

        WishProduct(
            user    = wishing_user,
            product = wished_product
        ).save()

        return JsonResponse(
            {'MESSAGE':'Added to the wishlist'},
            status = 200
        )

class ShowWishView(View):

    def get(self, request):
        data = json.loads(request.body)
        wish_items = WishProduct.objects.filter(id = data['user_id']).values()
        item_list = [item for item in wish_items]

        return JsonResponse(
            {'WISH LIST': item_list},
            status = 200
        )