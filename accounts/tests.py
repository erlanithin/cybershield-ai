from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login_and_logout(self):
        user = User.objects.create_user(username='loginuser', password='password123')
        # Login
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        # Logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
