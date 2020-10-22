from django.urls import path
from order.views import ReviewUploadView, ReviewShowView, AddWishView, ShowWishView, PlaceOrderView

urlpatterns = [
    path('reviewupload', ReviewUploadView.as_view()),
    path('reviewshow', ReviewShowView.as_view()),
    path('wishadd', AddWishView.as_view()),
    path('wishshow', ShowWishView.as_view()),
    path('placeorder', PlaceOrderView.as_view())
]
