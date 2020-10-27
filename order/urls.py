from django.urls import path
from order.views import CartView, CheckoutView, ShowOrdersView, DetailOrderView, WishView


urlpatterns = [
    path('/cart',                            CartView.as_view()),
    path('/checkout',                        CheckoutView.as_view()),
    path('/purchase/list',                   ShowOrdersView.as_view()),
    path('/purchase/detail/<int:order_id>',  DetailOrderView.as_view()),
    path('/wishlist',                        WishView.as_view()),
    # path('recent',                          RecentlyViewedView.as_view())
]