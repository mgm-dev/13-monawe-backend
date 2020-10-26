import json

from django.http    import JsonResponse
from django.views   import View

from order.models   import OrderStatus, Order, OrderProduct, DeliveryInfo, WishProduct, ViewedProduct
from user.models    import User, Address
from product.models import Product, ProductOption

# Create your views here.

# Add to cart
class CartView(View):

    # add the product into the cart
    def post(self, request):
        data = json.loads(request.body)

        # if the user has no cart yet, create the cart first
        if not Order.objects.filter(user = data['user_id']).exists():

            ordering_user = User.objects.get(id = data['user_id'])
            order_status  = OrderStatus.objects.get(id = 1)

            Order(
                user         = ordering_user,
                order_status = order_status
            ).save()
        
        target_cart             = Order.objects.get(user = data['user_id'])
        target_product_option   = ProductOption.objects.get(id = data['product_option_id'])
        target_product          = Product.objects.get(id = target_product_option.product_id)

        if OrderProduct.objects.filter(order = target_cart, product_option = target_product_option).exists():
            return JsonResponse(
                {'MESSAGE': 'This product already exists in the cart'},
                status = 404
            )

        else:
            OrderProduct(
                order           = target_cart,
                product         = target_product,
                product_option  = target_product_option,
                product_amount  = data['amount']
            ).save()

            return JsonResponse(
                {'MESSAGE': 'PRODUCT ADDED'},
                status = 201
            )

    def get(self, request):
        data             = json.loads(request.body)
        target_cart      = Order.objects.get(user = data['user_id'])
        products_in_cart = OrderProduct.objects.filter(order = target_cart).values()
        product_list     = [product for product in products_in_cart]

        return JsonResponse(
            {'PRODUCTS LIST': product_list},
            status = 200
        )

    # change the total amount
    def patch(self, request):
        data            = json.loads(request.body)
        target_cart     = Order.objects.get(user = data['user_id'])
        product_in_cart = OrderProduct.objects.filter(product_option = data['product_option_id'], order = target_cart)

        product_in_cart.update(product_amount = data['amount'])

        return JsonResponse(
            {'MESSAGE':'AMOUNT CHANGED'},
            status = 200
        )


    def delete(self, request):
        data = json.loads(request.body)
        OrderProduct.objects.get(id = data['order_product_id']).delete()

        return JsonResponse(
            {'MESSAGE': 'PRODUCT DELETED'},
            status=200
        )

# Place an order
class PlaceOrderView(View):

    def patch(self, request):  # update values which are NULL
        data             = json.loads(request.body)
        order_status     = OrderStatus.objects.get(id = 2)
        delivery_address = Address.objects.get(id = data['address_id'])
        target_cart      = Order.objects.get(id = data['cart_id'])

        target_cart.address         = delivery_address
        target_cart.order_request   = data['request']
        target_cart.date            = data['date']
        target_cart.order_status    = order_status
        target_cart.save()

        return JsonResponse(
            {'MESSAGE': 'ORDERED'},
            status=200
        )

# class ReviewUploadView(View):

#     def post(self, request):
#         data            = json.loads(request.body)
#         target_product  = Product.objects.get(id = data['product_id'])

#         if ProductReview.objects.filter(product = data['product_id'], user = data['user_id']).exists():
#             return JsonResponse(
#                 {'MESSAGE': 'Already wrote a review for this product'},
#                 status = 404
#             )
        
#         else:
#             ProductReview(
#                 user        = User.objects.get(id = data['user_id']),
#                 product     = target_product,
#                 rating      = data['rating'],
#                 title       = data['title'],
#                 content     = data['content'],
#                 created_at  = data['created_at'],
#                 updated_at  = data['updated_at'],
#                 image_url   = data['image_url'],
#             ).save()

#             return JsonResponse(
#                 {'MESSAGE':'Review uploaded'},
#                 status = 201
#             )

# class ReviewShowView(View):
    
#     def get(self, request, product_id):

#         review_data = ProductReview.objects.filter(product = product_id).values()
#         review_list = [review for review in review_data]

#         return JsonResponse(
#             {'REVIEWS': review_list},
#             status = 200
#         )

class WishView(View):

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

    def get(self, request):
        data            = json.loads(request.body)
        wish_products   = WishProduct.objects.filter(user = data['user_id']).values()
        product_list    = [product for product in wish_products]

        return JsonResponse(
            {'WISH LIST': product_list},
            status = 200
        )
    
    def delete(self, request):
        data = json.loads(request.body)
        WishProduct.objects.get(user = data['user_id'], product = data['product_id']).delete()

        return JsonResponse(
            {'MESSAGE': 'PRODUCT DELETED'},
            status = 200
        )

class RecentlyViewedView(View):
    
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
            status = 200)

    def get(self, request):
        data            = json.loads(request.body)
        viewed_products = WishProduct.objects.filter(id = data['user_id']).values()
        product_list    = [product for product in viewed_products]

        return JsonResponse(
            {'VIEWED LIST': product_list},
            status = 200
        )