from django.urls import path
from order.views import CartView, ReviewView, WishView, RecentlyViewedView

urlpatterns = [
    path('cart',            CartView.as_view()),
    path('review',          ReviewView.as_view()),
    path('wishlist',        WishView.as_view()),
    path('recentlyviewed',  RecentlyViewedView.as_view())
]
