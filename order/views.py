# autopep8: off
import json
import utils

from django.http    import JsonResponse
from django.views   import View


from order.models   import OrderStatus, Order, OrderProduct, WishProduct, ViewedProduct
from user.models    import User, Address
from product.models import Product, ProductOption

# Create your views here.

# Add to cart
class CartView(View):

    # @utils.signin_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = request.user.id
            chosen_products = data['chosen_product']

            target_cart, flag = Order.objects.get_or_create(user_id=user_id,
                                                            order_status_id=1)
            target_options = [chosen_products[i]["product_option_id"]
                              for i in range(0, len(chosen_products))]

            for option in target_options:
                if OrderProduct.objects.filter(order=target_cart.id,
                                               product_option=option).exists():

                    return JsonResponse(
                        {'message': 'ALREADY_EXISTS'},
                        status=409)

            target_products = [ProductOption.objects.get(id=target_options[i]).product_id
                               for i in range(0, len(target_options))]

            target_amount = [chosen_products[i]['amount']
                             for i in range(0, len(chosen_products))]

            for j in range(0, len(target_options)):
                OrderProduct(
                    product_amount=target_amount[j],
                    order_id=target_cart.id,
                    product_id=target_products[j],
                    product_option_id=target_options[j]
                ).save()

            return JsonResponse(
                {"message": "PRODUCT_ADDED"},
                status=201
            )

        except KeyError:
            return JsonResponse(
                {"message": "KEY_ERROR"},
                status=400
            )

    # @utils.signin_decorator
    def get(self, request):
        user_id          = request.user.id
        target_order     = Order.objects.get(user=user_id, order_status=1)
        products_in_cart = [products for products in Order.objects.get(
            user=user_id, order_status=1
        ).orderproduct_set.all().values()]

        product_in_cart = [products['product_id']
                           for products in products_in_cart]
        product_option_in_cart = [products["product_option_id"]
                                  for products in products_in_cart]

        product_name_list = [Product.objects.get(id=p_id).name
                             for p_id in product_in_cart]
        product_thumbnail_list = [Product.objects.get(id=p_id).thumb_nail
                                  for p_id in product_in_cart]
        product_bodycolor_list = [ProductOption.objects.get(id=p_id).body_color.name
                                  for p_id in product_option_in_cart]
        product_price_list = [Product.objects.get(id=p_id).price
                              for p_id in product_in_cart]
        product_plusprice_list = [ProductOption.objects.get(id=p_id).plus_price
                                  for p_id in product_option_in_cart]
        product_company_list = [Product.objects.get(id=p_id).company
                                for p_id in product_in_cart]

        list_per_product = []
        for i in range(0, len(products_in_cart)):
            product_price = product_price_list[i] + product_plusprice_list[i]
            product_amount = OrderProduct.objects.get(
                product_option=product_option_in_cart[i],
                order=target_order
            ).product_amount
            total_price = product_amount * product_price

            product_detail = {
                "product_option_id": product_option_in_cart[i],
                "product_name": product_name_list[i],
                "product_thumbnail": product_thumbnail_list[i],
                "product_bodycolor": product_bodycolor_list[i],
                "product_price": product_price,
                "product_company": product_company_list[i],
                "product_amount": product_amount,
                "total_price": total_price
            }
            list_per_product.append(product_detail)

        total_sum = 0
        for i in range(0, len(list_per_product)):
            total_sum = total_sum + int(list_per_product[i]["total_price"])

        return JsonResponse(
            {"product_detail": list_per_product,
             "total_sum": total_sum},
            status=200
        )
    # change the total amount

    @utils.signin_decorator
    def patch(self, request, product_option_id):
        try:
            data        = json.loads(request.body)
            user_id     = request.user.id
            target_cart = Order.objects.get(user=user_id, order_status=1)

            target_product  = ProductOption.objects.get(id=product_option_id)
            product_in_cart = OrderProduct.objects.get(
                product_option=product_option_id,
                order=target_cart)
            product_price = (target_product.plus_price
                             + Product.objects.get(id=target_product.product_id).price)
            product_in_cart.product_amount = data['amount']
            new_price = product_in_cart.product_amount * product_price

            return JsonResponse(
                {"message": "AMOUNT_CHANGED",
                 "total_price": new_price},
                status=200
            )

        except KeyError:
            return JsonResponse(
                {"message": "KEY_ERROR"},
                status=400
            )

    @utils.signin_decorator
    def delete(self, request, product_option_id):
        user_id     = request.user.id
        target_cart = Order.objects.get(user=user_id, order_status=1)

        OrderProduct.objects.filter(
            product_option=product_option_id, order=target_cart).delete()
        # to show the remaining items
        target_order     = Order.objects.get(user=user_id, order_status=1)
        products_in_cart = [products for products in Order.objects.get(
            user=user_id, order_status=1
        ).orderproduct_set.all().values()]

        product_in_cart = [products['product_id']
                           for products in products_in_cart]
        product_option_in_cart = [products["product_option_id"]
                                  for products in products_in_cart]

        product_name_list = [Product.objects.get(id=p_id).name
                             for p_id in product_in_cart]
        product_thumbnail_list = [Product.objects.get(id=p_id).thumb_nail
                                  for p_id in product_in_cart]
        product_bodycolor_list = [ProductOption.objects.get(id=p_id).body_color.name
                                  for p_id in product_option_in_cart]
        product_price_list = [Product.objects.get(id=p_id).price
                              for p_id in product_in_cart]
        product_plusprice_list = [ProductOption.objects.get(id=p_id).plus_price
                                  for p_id in product_option_in_cart]
        product_company_list = [Product.objects.get(id=p_id).company
                                for p_id in product_in_cart]

        list_per_product = []
        for i in range(0, len(products_in_cart)):
            product_detail = {
                "product_option_id": product_option_in_cart[i],
                "product_name"     : product_name_list[i],
                "product_thumbnail": product_thumbnail_list[i],
                "product_bodycolor": product_bodycolor_list[i],
                "product_price"    : product_price_list[i] + product_plusprice_list[i],
                "product_company"  : product_company_list[i],
                "product_amount"   : OrderProduct.objects.get(
                    product_option=product_option_in_cart[i],
                    order=target_order
                ).product_amount
            }
            list_per_product.append(product_detail)

        return JsonResponse(
            {"message": "DELETED",
             "product_detail": list_per_product},
            status=200
        )


# class CheckoutView(View):

#     def patch(self, request, order_id):
#         delivery_address = Address.objects.get(id = data['address_id'])
#         order_status     = 2

#         target_cart                 = Order.objects.get(id = order_id)
#         target_cart.address         = delivery_address
#         target_cart.order_request   = data['request']
#         target_cart.order_status    = order_status
#         target_cart.save()

#         return JsonResponse(
#             {'message': 'ORDERED'},
#             status=200
#         )


# class ShowOrdersView(View):
#     @utils.signin_decorator
#     def get(self, request):
#         data            = json.loads(request.body)
#         user_id = request.user.id
#         all_orders      = [order for order in Order.objects.filter(user = user_id).values()]

#         return JsonResponse(
#             {'order_list': all_orders},
#             status = 200
#         )


# class DetailOrderView(View):

#     def get(self, request, order_id):
#         ordered_products   = [product for product in OrderProduct.objects.filter(order = order_id).values()]

#         return JsonResponse(
#             {'product_list':ordered_products},
#             status = 200
#         )


class WishView(View):
    @utils.signin_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = request.user.id

            if WishProduct.objects.filter(user=user_id, product=data['product_id']).exists():
                WishProduct.objects.get(
                    user=user_id, product=data['product_id']).delete()

                return JsonResponse(
                    {'message': 'REMOVED'},
                    status=200
                )

            else:
                WishProduct(
                    user_id=user_id,
                    product_id=data['product_id']
                ).save()

                return JsonResponse(
                    {"message": "ADDED_TO_WISHLIST"},
                    status=201
                )

        except KeyError:
            return JsonResponse(
                {"message": "KEY_ERROR"},
                status=400
            )

    @utils.signin_decorator
    def get(self, request):
        user_id = request.user.id
        wish_products = [
            product for product in WishProduct.objects.filter(user=user_id).values()]
        wish_product = [products['product_id'] for products in wish_products]

        product_name_list = [Product.objects.get(
            id=p_id).name for p_id in wish_product]
        product_thumbnail_list = [Product.objects.get(
            id=p_id).thumb_nail for p_id in wish_product]
        product_price_list = [Product.objects.get(
            id=p_id).price for p_id in wish_product]
        product_company_list = [Product.objects.get(
            id=p_id).company for p_id in wish_product]

        list_per_product = []
        for i in range(0, len(wish_products)):
            product_detail = {
                "product_id": wish_product[i],
                "product_name": product_name_list[i],
                "product_thumbnail": product_thumbnail_list[i],
                "product_price": product_price_list[i],
                "product_company": product_company_list[i]
            }

            list_per_product.append(product_detail)

        return JsonResponse(
            {'wish_list': list_per_product},
            status=200
        )

    @utils.signin_decorator
    def delete(self, request, product_id):
        data = json.loads(request.body)
        user_id = request.user.id
        WishProduct.objects.get(user=user_id, product=product_id).delete()

        wish_products = [
            product for product in WishProduct.objects.filter(user=user_id).values()]
        wish_product = [products['product_id'] for products in wish_products]

        product_name_list = [Product.objects.get(
            id=p_id).name for p_id in wish_product]
        product_thumbnail_list = [Product.objects.get(
            id=p_id).thumb_nail for p_id in wish_product]
        product_price_list = [Product.objects.get(
            id=p_id).price for p_id in wish_product]
        product_company_list = [Product.objects.get(
            id=p_id).company for p_id in wish_product]

        list_per_product = []
        for i in range(0, len(wish_products)):
            product_detail = {
                "product_id": wish_product[i],
                "product_name": product_name_list[i],
                "product_thumbnail": product_thumbnail_list[i],
                "product_price": product_price_list[i],
                "product_company": product_company_list[i]
            }

            list_per_product.append(product_detail)

        return JsonResponse(
            {'message': 'DELETED',
             'product_detail': list_per_product},
            status=204
        )


class RecentlyViewedView(View):
    @utils.signin_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = request.user.id
            view_user = User.objects.get(id=user_id)
            viewed_product = Product.objects.get(id=data['product_id'])

            ViewedProduct(
                user=view_user,
                product=viewed_product
            ).save()

            return JsonResponse(
                {"message": "ADDED_TO_VIEWED_LIST"},
                status=200)

        except KeyError:
            return JsonResponse(
                {"message": "KEY_ERROR"},
                status=400
            )

    @utils.signin_decorator
    def get(self, request):
        user_id = request.user.id
        viewed_products = ViewedProduct.objects.filter(user=user_id).values()
        product_list = [product for product in viewed_products]

        if len(product_list) > 10:
            product_list_ten = product_list[len(product_list)-10:]

        else:
            product_list_ten = product_list

        print(product_list_ten)

        image_list = [Product.objects.get(id=product_list_ten[i]['product_id']).thumb_nail
                      for i in range(0, len(product_list_ten))]
        name_list = [Product.objects.get(id=product_list_ten[i]['product_id']).name
                     for i in range(0, len(product_list_ten))]
        price_list = [Product.objects.get(id=product_list_ten[i]['product_id']).price
                      for i in range(0, len(product_list_ten))]

        showing_list = []
        for i in reversed(range(0, len(product_list_ten))):
            product_detail = {
                "product_image": image_list[i],
                "product_name": name_list[i],
                "product_price": price_list[i]
            }
            showing_list.append(product_detail)

        return JsonResponse(
            {"viewed_list": showing_list},
            status=200
        )
