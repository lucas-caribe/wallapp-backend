from django.urls import path, include

urlpatterns = [
  path('users/', include('dj_rest_auth.urls')),
  path('users/registration/', include('dj_rest_auth.registration.urls')),
]
