import json

from django.http    import JsonResponse
from django.views   import View


from order.models   import OrderStatus, Order, OrderProduct, WishProduct, ViewedProduct
from user.models    import User, Address
from product.models import Product, ProductOption

# Create your views here.

# Order
class CartView(View):
    # add the product into the cart
    def post(self, request):
        data = json.loads(request.body)
        # if the user has no cart yet, create the cart first
        if not (Order.objects.filter(user = data['user_id'], order_status = 1).exists()):
            Order(
                user_id         = data['user_id'],
                order_status_id = 1
            ).save()
    
        target_cart             = Order.objects.get(order_status = 1, user = data['user_id'])
        target_product_option   = ProductOption.objects.get(id = data['product_option_id'])
        target_product          = Product.objects.get(id = target_product_option.product_id)

        if OrderProduct.objects.filter(order = target_cart, product_option = target_product_option).exists():

            return JsonResponse(
                {'message': 'ALREADY_EXISTS'},
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
                {'message': 'PRODUCT_ADDED'},
                status = 201
            )
    #프로덕트 설명이 없음.. 다 풀어서 보내기
    def get(self, request):
        data             = json.loads(request.body)
        products_in_cart = [products for products in Order.objects.get(
                           user = data['user_id'], order_status = 1
                           ).orderproduct_set.all().values()]

        target_order = Order.objects.get(user = data['user_id'], order_status = 1)
        
        product_in_cart        = [products['product_id'] for products in products_in_cart]
        product_option_in_cart = [products["product_option_id"] for products in products_in_cart]

        product_name_list       = [Product.objects.get(id = p_id).name for p_id in product_in_cart]
        product_thumbnail_list  = [Product.objects.get(id = p_id).thumb_nail for p_id in product_in_cart]
        product_bodycolor_list  = [ProductOption.objects.get(id = p_id).body_color.name for p_id in product_option_in_cart]
        # product_inkcolor_list   = [ProductOption.objects.get(id = p_id).ink_color.name for p_id in product_option_in_cart]
        # product_thickness_list  = [ProductOption.objects.get(id = p_id).thickness.value for p_id in product_option_in_cart]
        product_price_list      = [Product.objects.get(id = p_id).price for p_id in product_in_cart]
        product_plusprice_list  = [ProductOption.objects.get(id = p_id).plus_price for p_id in product_option_in_cart]
        product_company_list    = [Product.objects.get(id = p_id).company for p_id in product_in_cart]

        list_per_product = []

        for i in range(0, len(products_in_cart)):
            product_detail = {
                "product_option_id"    : product_option_in_cart[i],
                "product_name"         : product_name_list[i],
                "product_thumbnail"    : product_thumbnail_list[i],
                "product_bodycolor"    : product_bodycolor_list[i], 
                # "product_inkcolor"     : product_inkcolor_list[i],
                # "product_thickness"    : product_thickness_list[i], 
                "product_price"        : product_price_list[i] + product_plusprice_list[i],
                "product_company"      : product_company_list[i],
                "product_amount"       : OrderProduct.objects.get(
                    product_option = product_option_in_cart[i], 
                    order = target_order
                    ).product_amount
            }
            list_per_product.append(product_detail)

        return JsonResponse(
            {'product_detail' : list_per_product},
            status = 200
        )
    # change the total amount
    def patch(self, request, product_option_id):
        data            = json.loads(request.body)
        target_cart     = Order.objects.get(user = data['user_id'], order_status = 1)
        product_in_cart = OrderProduct.objects.filter(product_option = product_option_id, order = target_cart)

        product_in_cart.update(product_amount = data['amount'])

        return JsonResponse(
            {'message':'AMOUNT_CHANGED'},
            status = 200
        )

    def delete(self, request, product_option_id):
        data            = json.loads(request.body)
        target_cart     = Order.objects.get(user = data['user_id'], order_status = 1)
        OrderProduct.objects.filter(product_option = product_option_id, order = target_cart).delete()

        return JsonResponse(
            {'message': 'DELETED'},
            status=204
        )


class CheckoutView(View):
    # when a user places an orderfilter
    def patch(self, request, order_id):
        delivery_address = Address.objects.get(id = data['address_id'])
        order_status     = 2

        target_cart                 = Order.objects.get(id = order_id)
        target_cart.address         = delivery_address
        target_cart.order_request   = data['request']
        target_cart.order_status    = order_status
        target_cart.save()

        return JsonResponse(
            {'message': 'ORDERED'},
            status=200
        )


class ShowOrdersView(View):

    def get(self, request):
        data            = json.loads(request.body)
        all_orders      = [order for order in Order.objects.filter(user = data['user_id']).values()]

        return JsonResponse(
            {'order_list': all_orders},
            status = 200
        )


class DetailOrderView(View):

    def get(self, request, order_id):
        ordered_products   = [product for product in OrderProduct.objects.filter(order = order_id).values()]

        return JsonResponse(
            {'product_list':ordered_products},
            status = 200
        )


class WishView(View):

    def post(self, request):
        data            = json.loads(request.body)

        if WishProduct.objects.filter(user = data['user_id'], product = data['product_id']).exists():
            return JsonResponse(
                {'message': 'The product already exists in the wishlist'},
                status = 404
            )

        else:
            WishProduct(
                user_id    = data['user_id'],
                product_id = data['product_id']
            ).save()

            return JsonResponse(
                {'message':'ADDED_TO_WISHLIST'},
                status = 201
            )

    def get(self, request):
        data            = json.loads(request.body)
        wish_products   = [product for product in WishProduct.objects.filter(user = data['user_id']).values()]

        wish_product = [products['product_id'] for products in wish_products]

        product_name_list = [Product.objects.get(id = p_id).name for p_id in wish_product]
        product_thumbnail_list = [Product.objects.get(id = p_id).thumb_nail for p_id in wish_product]
        product_price_list = [Product.objects.get(id = p_id).price for p_id in wish_product]
        product_company_list = [Product.objects.get(id = p_id).company for p_id in wish_product]

        list_per_product = []

        for i in range(0, len(wish_products)):
            product_detail = {
                "product_id"    : wish_product[i],
                "product_name"  : product_name_list[i],
                "product_thumbnail" : product_thumbnail_list[i],
                "product_price" : product_price_list[i],
                "product_company" : product_company_list[i]
            }

            list_per_product.append(product_detail)

        return JsonResponse(
            {'wish_list': list_per_product},
            status = 200
        )
    
    def delete(self, request, product_id):
        data = json.loads(request.body)
        WishProduct.objects.get(user = data['user_id'], product = product_id).delete()

        return JsonResponse(
            {'message': 'DELETED'},
            status = 204
        )


# class RecentlyViewedView(View):
#     def post(self, request):
#         data            = json.loads(request.body)
#         view_user       = User.objects.get(id = data['user_id'])
#         viewed_product  = Product.objects.get(id = data['product_id'])

#         ViewedProduct(
#             user    = view_user,
#             product = viewed_product
#         ).save()

#         return JsonResponse(
#             {'MESSAGE':'Added to the viewed list'},
#             status = 200)

#     def get(self, request):
#         data            = json.loads(request.body)
#         viewed_products = ViewedProduct.objects.filter(user = data['user_id']).values()
#         product_list    = [product for product in viewed_products]

#         return JsonResponse(
#             {'VIEWED LIST': product_list},
#             status = 200
#         )