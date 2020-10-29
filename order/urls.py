from django.urls import path
from order.views import CartView, WishView, RecentlyViewedView


urlpatterns = [
    path('/cart',                            CartView.as_view()),
    path('/cart/<int:product_option_id>',    CartView.as_view()),
    # path('/checkout/<int:order_id>',         CheckoutView.as_view()),
    # path('/purchase/list',                   ShowOrdersView.as_view()),
    # path('/purchase/detail/<int:order_id>',  DetailOrderView.as_view()),
    path('/wishlist',                        WishView.as_view()),
    path('/wishlist/<int:product_id>',       WishView.as_view()),
    path('/recent',                          RecentlyViewedView.as_view())
]