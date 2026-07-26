import shutil
import tempfile
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Transaction


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TransactionReceiptTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='receipt-user',
            password='test-password',
        )
        self.other_user = get_user_model().objects.create_user(
            username='other-receipt-user',
            password='test-password',
        )
        self.transaction = Transaction.objects.create(
            user=self.user,
            title='Textbook',
            amount=Decimal('80.00'),
            transaction_type=Transaction.EXPENSE,
            category='education',
            date=timezone.localdate(),
        )
        self.transaction.receipt.save('receipt.pdf', ContentFile(b'%PDF-1.4 test'), save=True)

    def test_receipt_requires_login(self):
        response = self.client.get(reverse('transaction_receipt', args=[self.transaction.pk]))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('transaction_receipt', args=[self.transaction.pk])}",
        )

    def test_owner_can_view_receipt(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('transaction_receipt', args=[self.transaction.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_other_user_cannot_view_receipt(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse('transaction_receipt', args=[self.transaction.pk]))
        self.assertEqual(response.status_code, 404)
