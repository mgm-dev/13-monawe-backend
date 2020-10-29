from django.urls import path
<<<<<<< HEAD

urlpatterns = []
=======
from product.views import Detail, ProductList

urlpatterns = [
    path('s', ProductList.as_view()),
    path('/<int:product_id>', Detail.as_view())
]
>>>>>>> bde81ab1bd76595fae84451c3123e83ebe5e5adc
