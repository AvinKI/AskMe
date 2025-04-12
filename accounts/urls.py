from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path(' ', index, name='home'),
    path('login/', login_view, name='login'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    # path('logout/', CustomLogoutView.as_view(), name='logout'),
]
