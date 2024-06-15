# transactions/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer

class TransactionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.transaction = Transaction.objects.create(user=self.user, amount=100.0, status='PENDING')

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.amount, 100.0)
        self.assertEqual(self.transaction.status, 'PENDING')

    def test_transaction_processing_success(self):
        self.transaction.process_transaction()
        self.assertEqual(self.transaction.status, 'SUCCESS')

    def test_transaction_processing_failure(self):
        self.transaction.amount = -10.0
        self.transaction.process_transaction()
        self.assertEqual(self.transaction.status, 'FAILED')

class TransactionSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.transaction_data = {'user': self.user.id, 'amount': 100.0, 'status': 'PENDING'}
        self.serializer = TransactionSerializer(data=self.transaction_data)

    def test_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serializer_invalid_amount(self):
        self.transaction_data['amount'] = -10.0
        serializer = TransactionSerializer(data=self.transaction_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount', serializer.errors)

class TransactionViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.transaction_data = {'user': self.user.id, 'amount': 100.0, 'status': 'PENDING'}
        self.transaction = Transaction.objects.create(user=self.user, amount=100.0, status='PENDING')
        self.url = reverse('transaction-list')

    def test_create_transaction(self):
        response = self.client.post(self.url, self.transaction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_transactions(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
