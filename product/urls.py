from django.urls import path
from product.views import Detail, ProductList, Review

urlpatterns = [
    path('list', ProductList.as_view()),
    path('detail/<int:product_id>', Detail.as_view()),
    path('review', Review.as_view())
]
