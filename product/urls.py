from django.urls import path
from product.views import All, Category, Subcategory, Detail, Search

urlpatterns = [
    path('all', All.as_view()),
    path('category/<int:category_id>', Category.as_view()),
    path('subcategory/<int:subcategory_id>', Subcategory.as_view()),
    path('detail/<int:product_id>', Detail.as_view()),
    path('search', Search.as_view())
]
