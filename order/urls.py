from django.urls import path
from order.views import *

urlpatterns = [
    path('createcart',      CreateCartView.as_view()),
    path('addproduct',      AddProductView.as_view()),
    path('placeorder',      PlaceOrderView.as_view()),
    path('deleteproduct',   DeleteProductView.as_view()),

    path('reviewupload',    ReviewUploadView.as_view()),
    path('reviewshow',      ReviewShowView.as_view()),
    path('wishadd',         AddWishView.as_view()),
    path('wishshow',        ShowWishView.as_view()),
    path('viewedadd',       AddViewedProduct.as_view()),
    path('viewedshow',      ShowViewedProduct.as_view())
]
