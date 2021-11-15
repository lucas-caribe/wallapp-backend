from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    registration_url = reverse('user-registration')
    login_url = reverse('rest_login')

    USERNAME = 'lucas'
    EMAIL = 'lucas@email.com'
    PASSWORD = 'password123..'

    registration_data = {
        'username': USERNAME,
        'email': EMAIL,
        'password1': PASSWORD,
        'password2': PASSWORD,
    }

    login_data = {
        'username': USERNAME,
        'password': PASSWORD,
    }

    email_subject = 'Welcome to WallApp!'
    email_body = (f'Hi, {USERNAME}!\n\nYour account was successfully created! '
        'Thank you for registering at WallApp!')

    # user should be able to register
    def test_registration(self):
        user_count = User.objects.all().count()

        response = self.client.post(
            self.registration_url, self.registration_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), user_count + 1)

    # user should recieve a welcome email after registration
    def test_welcome_email(self):
        response = self.client.post(
            self.registration_url, self.registration_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, self.email_subject)
        self.assertEqual(mail.outbox[0].body, self.email_body)

    # user should be able to login after registration
    def test_login(self):
        response = self.client.post(
            self.registration_url, self.registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
