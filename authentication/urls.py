from django.urls import path
from authentication.views import *

urlpatterns = [
    path("register/" ,registerView,name="registerView"),
    path("login/",loginView,name="loginView"),
    path("logout/",logoutView,name="logoutView")
]