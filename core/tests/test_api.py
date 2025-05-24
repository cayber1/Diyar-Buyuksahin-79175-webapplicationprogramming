from django.urls import reverse
from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Post

class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        data = {'title': 'Test Başlık', 'content': 'Test içerik'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post_list(self):
        Post.objects.create(title='Post 1', content='İçerik 1')
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_post(self):
        post = Post.objects.create(title='Eski Başlık', content='Eski içerik')
        url = f'/api/posts/{post.id}/'
        data = {'title': 'Yeni Başlık', 'content': 'Yeni içerik'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Yeni Başlık')

    def test_delete_post(self):
        post = Post.objects.create(title='Silinecek', content='...')
        url = f'/api/posts/{post.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
