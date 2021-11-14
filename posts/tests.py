from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post

class PostTests(APITestCase):
  registration_url = reverse('user-registration')
  login_url = reverse('rest_login')
  post_url = reverse('post-list')
  
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
  
  post_data = {
    'body': 'this is a sample post',
  }

  # guests should be able to view posts
  def test_guest_view(self):
    user = User.objects.create(username=self.USERNAME, password=self.PASSWORD)
    post = Post.objects.create(body='nothing here', owner=user)

    response = self.client.get(self.post_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['body'], post.body)

  # guests should not be able to create posts
  def test_guest_permissions(self):
    response = self.client.post(self.post_url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

  # logged users should be able to create posts
  def test_user_post(self):
    # registration
    response = self.client.post(self.registration_url, self.registration_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # login
    response = self.client.post(self.login_url, self.login_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # create post
    token = response.data['key']

    response = self.client.post(
      self.post_url,
      self.post_data,
      HTTP_AUTHORIZATION=f'Token {token}',
      format='json'
    )
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['body'], self.post_data['body'])
    self.assertEqual(response.data['owner'], self.USERNAME)
