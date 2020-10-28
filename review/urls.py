# autopep8: off
from django.urls  import path
from review.views import Review

urlpatterns = [
    path('', Review.as_view())
]
