from django.urls import path
from order.views import CartView, PlaceOrderView, WishView, RecentlyViewedView, ShowOrdersView, DetailOrderView


urlpatterns = [
    path('cart',                        CartView.as_view()),
    path('checkout',                    CheckoutView.as_view()),
    path('list',                        ShowOrdersView.as_view()),
    path('detail/<int:order_id>',       DetailOrderView.as_view()),
    path('wishlist',                    WishView.as_view()),
    path('recent',                      RecentlyViewedView.as_view())
]