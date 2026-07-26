from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from transactions.models import Transaction


class CorePageTests(TestCase):
    def test_public_pages_load(self):
        for url_name in ('home', 'about', 'contact'):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_dashboard_loads_for_authenticated_user(self):
        user = get_user_model().objects.create_user(
            username='dashboard-user',
            password='test-password',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('income_total', response.context)

    def test_initial_data_fixture_loads(self):
        call_command('loaddata', 'initial_data', verbosity=0)

        self.assertTrue(get_user_model().objects.filter(username='demo_user').exists())
        self.assertTrue(Transaction.objects.filter(title='Salary').exists())
