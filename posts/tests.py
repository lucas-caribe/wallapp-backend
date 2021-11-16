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

    post_update_data = {
        'body': 'this is an updated post',
    }

    # guests should be able to view posts
    def test_guest_view(self):
        user = User.objects.create(
            username=self.USERNAME, password=self.PASSWORD)
        post = Post.objects.create(body='nothing here', owner=user)

        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['body'], post.body)

    # guests should not be able to create posts
    def test_guest_permissions(self):
        response = self.client.post(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.'
        )

    # logged users should be able to create, update and delete posts
    def test_user_crud(self):
        # registration
        response = self.client.post(
            self.registration_url, self.registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # login
        response = self.client.post(
            self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['key']

        # create post
        AUTHORIZATION = f'Token {token}'

        response = self.client.post(
            self.post_url,
            self.post_data,
            HTTP_AUTHORIZATION=AUTHORIZATION
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['body'], self.post_data['body'])
        self.assertEqual(response.data['owner'], self.USERNAME)

        # update post
        update_delete_post_url = f'{self.post_url}1/'

        response = self.client.put(
            update_delete_post_url,
            self.post_update_data,
            HTTP_AUTHORIZATION=AUTHORIZATION
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], self.post_update_data['body'])

        updated_post = Post.objects.get(pk=1)
        self.assertEqual(updated_post.body, self.post_update_data['body'])

        # delete post
        response = self.client.delete(
            update_delete_post_url,
            HTTP_AUTHORIZATION=AUTHORIZATION,
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        post_count = Post.objects.all().count()
        self.assertEqual(post_count, 0)

    # logged users should only be able to edit or delete their own posts
    def test_user_owner_permissions(self):
        user = User.objects.create(
            username='shrek', password='shrek123..')
        post = Post.objects.create(body='Ogres Are Like Onions', owner=user)

        # registration
        self.client.post(
            self.registration_url, self.registration_data)

        # login
        response = self.client.post(
            self.login_url, self.login_data)

        token = response.data['key']

        # trying to update post
        AUTHORIZATION = f'Token {token}'

        update_delete_post_url = f'{self.post_url}1/'

        response = self.client.put(
            update_delete_post_url,
            self.post_update_data,
            HTTP_AUTHORIZATION=AUTHORIZATION,
        )

        check_post = Post.objects.get(pk=1)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(check_post.body, 'Ogres Are Like Onions')

        # trying to delete post
        response = self.client.delete(
            update_delete_post_url,
            HTTP_AUTHORIZATION=AUTHORIZATION,
        )

        post_count = Post.objects.all().count()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(post_count, 1)
