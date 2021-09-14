from django.urls import  path
from . import views

app_name = "usuarios"

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.Register.as_view(), name="register"),
    path('profile/<int:pk>', views.Profile.as_view(), name="profile"),
    # path('profile', views.profile, name="profile"),
]
