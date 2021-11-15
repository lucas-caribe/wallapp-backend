from decouple import config
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView


def send_greetings_email(username, email):
    try:
        subject = 'Welcome to WallApp!'
        message = (f'Hi, {username}!\n\nYour account was successfully created! '
            'Thank you for registering at WallApp!')
        from_email = config('FROM_EMAIL')

        send_mail(subject, message, from_email, [email])
    except Exception as e:
        print(e.body)


class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        send_greetings_email(user.username, user.email)

        return Response(
            self.get_response_data(user),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
