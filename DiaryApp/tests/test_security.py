from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class CSRFSecurityTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_csrf_protection_on_create_entry(self):
        response = self.client.post(reverse('create_entry'), {
            'title': 'CSRF test',
            'content': 'Trying to submit without CSRF',
            'mood': 'happy',
        }, follow=True)

        # Проверяем: если CSRF токен отсутствует, должно быть 403
        self.assertEqual(response.status_code, 403)
