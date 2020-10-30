from django.urls import path
from product.views import Detail, ProductList


urlpatterns = [
    path('s', ProductList.as_view()),
    path('/<int:product_id>', Detail.as_view())
]
