from django.urls import path
<<<<<<< HEAD
from user.views import SignUp, SignIn, CheckEmail, CheckAccount, UserInfo, AddressView

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('signin', SignIn.as_view()),
    path('checkemail', CheckEmail.as_view()),
    path('checkaccount', CheckAccount.as_view()),
    path('userinfo', UserInfo.as_view()),
    path('address', AddressView.as_view()),
]
=======

urlpatterns = []
>>>>>>> bde81ab1bd76595fae84451c3123e83ebe5e5adc
