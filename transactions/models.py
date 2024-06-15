from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def process_transaction(self):
        """
        Simulate transaction processing logic.
        """
        if self.amount <= 0:
            self.status = 'FAILED'
        else:
            self.status = 'SUCCESS'
        self.save()

    def __str__(self):
        return f'Transaction {self.id} - {self.status}'
