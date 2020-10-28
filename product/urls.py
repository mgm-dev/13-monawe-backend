# from django.urls import path
# from product.views import All, Category, Subcategory

# urlpatterns = [
#     path('all', All.as_view()),
#     path('category/<int:category_id>', Category.as_view()),
#     path('subcategory/<int:subcategory_id>', Subcategory.as_view()),
# ]

from django.urls import path
from product.views import Detail, ProductList


urlpatterns = [
    path('s', ProductList.as_view()),
    path('/<int:product_id>', Detail.as_view())
]

