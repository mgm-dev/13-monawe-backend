from django.urls import path
from order.views import CartView, ReviewUploadView, ReviewShowView, WishView, RecentlyViewedView




urlpatterns = [
    path('cart',                    CartView.as_view()),
    path('review',                  ReviewUploadView.as_view()),
    path('review/<int:product_id>', ReviewShowView.as_view()),
    path('wishlist',                WishView.as_view()),
    path('recentlyviewed',          RecentlyViewedView.as_view())
]