
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Deal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='deals')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='В работе')
    currency = models.CharField(max_length=5, default='₽')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.client.name})"
