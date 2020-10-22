import json

from django.http    import JsonResponse
from django.views   import View

from order.models import *
from user.models import User, Address
from product.models import Product, ProductOption

# Create your views here.

# Order

# when a user adds products into the cart or places an order, an empty cart(virtual) should be created first.
class CreateCartView(View):

    def post(self, request):
        data            = json.loads(request.body)

        ordering_user   = User.objects.get(id = data['user_id'])
        order_status    = OrderStatus.objects.get(id = 1)

        Order(
            user            = ordering_user,
            # address         = NULL,
            # order_request   = NULL,
            # date            = NULL,
            order_status    = order_status
        ).save()

        return JsonResponse(
            {'MESSAGE':'Cart Created'},
            status = 201
        )

class AddProductView(View):  # when a user adds products in the cart

    def post(self, request):
        data                    = json.loads(request.body)
        target_cart             = Order.objects.get(id = data['cart_id'])
        target_product_option   = ProductOption.objects.get(id = data['product_option_id'])
        target_product          = Product.objects.get(id = target_product_option.product_id)

        # if the product already exists in the cart, the total amount of it is increased by 1
        if OrderProduct.objects.filter(product_option = data['product_option_id'], order = data['cart_id']).exists():
            OrderProduct.objects.filter(product_option = data['product_option_id'], order = data['cart_id']).update(product_amount = OrderProduct.objects.get(product_option = data['product_option_id'], order = data['cart_id']).product_amount + data['amount'])

            return JsonResponse(
                {'MESSAGE':'Amount Increased'},
                status = 200
            )

        else:
            OrderProduct(
                order           = target_cart,
                product         = target_product,
                product_option  = target_product_option,
                product_amount  = data['amount']
            ).save()

            return JsonResponse(
                {'MESSAGE': 'Added Product'},
                status = 201
            )

class PlaceOrderView(View):  # when a user places an order

    def PUT(self, request):  # update values which are NULL
        data            = json.loads(request.body)
        order_status    = Status.objects.get(id = 2)

        target_cart                 = Order.objects.get(id = data['cart_id'])
        target_cart.address         = data['address_id']
        target_cart.order_request   = data['request']
        target_cart.date            = data['date']
        target_cart.status          = order_status
        target_cart.save()

        return JsonResponse(
            {'MESSAGE': 'ORDERED'},
            status=200
        )

class DeleteProductView(View):  # delete per product_option

    def delete(self, request):
        data = json.loads(request.body)
        OrderProduct.objects.get(id = data['order_product_id']).delete()

        return JsonResponse(
            {'MESSAGE': 'DELETED'},
            status=200
        )


# Review
class ReviewUploadView(View):

    def post(self, request):
        data            = json.loads(request.body)
        target_product  = Product.objects.get(id = data['product_id'])

        if ProductReview.objects.filter(product = data['product_id'], user = data['user_id']).exists():
            return JsonResponse(
                {'MESSAGE': 'Already wrote a review for this product'},
                status = 404
            )
        
        else:
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
        wish_products = WishProduct.objects.filter(id = data['user_id']).values()
        product_list = [product for product in wish_products]

        return JsonResponse(
            {'WISH LIST': product_list},
            status = 200
        )

# recently viewed
class AddViewedProduct(View):

    def post(self, request):
        data            = json.loads(request.body)
        view_user       = User.objects.get(id = data['user_id'])
        viewed_product  = Product.objects.get(id = data['product_id'])

        WishProduct(
            user    = view_user,
            product = viewed_product
        ).save()

        return JsonResponse(
            {'MESSAGE':'Added to the viewed list'},
            status = 200
        )

class ShowViewedProduct(View):

    def get(self, request):
        data = json.loads(request.body)
        viewed_products = WishProduct.objects.filter(id = data['user_id']).values()
        product_list = [product for product in viewed_products]

        return JsonResponse(
            {'VIEWED LIST': product_list},
            status = 200
        )