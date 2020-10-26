from django.urls import path
from product.views import Detail, Search, ProductList

urlpatterns = [
    path('list', ProductList.as_view()),
    path('detail/<int:product_id>', Detail.as_view()),
    path('search', Search.as_view())
]
