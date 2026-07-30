from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import SavingsGoal


class SavingsGoalActionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='savings-user',
            password='test-password',
        )
        self.goal = SavingsGoal.objects.create(
            user=self.user,
            name='Car',
            target_amount=Decimal('5000.00'),
            current_amount=Decimal('400.00'),
        )

    def test_add_monthly_saving_updates_goal(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('savings_goal_add_contribution', args=[self.goal.pk]),
            {'amount': '250.00'},
        )

        self.assertRedirects(response, reverse('savings_goal_list'))
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.current_amount, Decimal('650.00'))
        self.assertFalse(self.goal.is_completed)

    def test_add_monthly_saving_caps_at_target_and_completes_goal(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('savings_goal_add_contribution', args=[self.goal.pk]),
            {'amount': '6000.00'},
        )

        self.assertRedirects(response, reverse('savings_goal_list'))
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.current_amount, Decimal('5000.00'))
        self.assertTrue(self.goal.is_completed)

    def test_complete_goal_sets_current_amount_to_target(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('savings_goal_complete', args=[self.goal.pk]))

        self.assertRedirects(response, reverse('savings_goal_list'))
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.current_amount, Decimal('5000.00'))
        self.assertTrue(self.goal.is_completed)
