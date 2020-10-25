from django.urls import path
from user.views import SignUp, SignIn, CheckEmail, CheckAccount, UserInfo

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('signin', SignIn.as_view()),
    path('checkemail', CheckEmail.as_view()),
    path('checkaccount', CheckAccount.as_view()),
    path('userinfo', UserInfo.as_view())
]
