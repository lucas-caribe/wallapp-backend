from django.urls import path, include
from .views import CustomRegisterView

urlpatterns = [
    path('users/', include('dj_rest_auth.urls')),
    path('users/registration/', CustomRegisterView.as_view(),
         name='user-registration'),
]
