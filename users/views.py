from rest_framework import status
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView

class CustomRegisterView(RegisterView):
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)

    return Response(
      self.get_response_data(user),
      status=status.HTTP_201_CREATED,
      headers=headers,
    )
