# from django.urls import path
# from . import views

# urlpatterns = [
#     path("posts/", views.post_list, name="post_list"),         # GET, POST
#     path("posts/<int:pk>/", views.post_detail, name="post_detail"),  # GET, PUT, DELETE
#     path('', views.home, name='home'), # Default Home Page 
# ]


# Here we add All Routes which are defined the Views.py files
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.home, name='home'),
    path("signup/", views.signup, name="signup"),  # new route for signup
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # JWT login
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # refresh token
    path("posts/", views.post_list, name="post_list"),
    path("posts/<int:pk>", views.post_detail, name="post_detail"),
    path('', views.home, name='home'), # Default Home Page 
]
