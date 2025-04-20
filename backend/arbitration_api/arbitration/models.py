from django.db import models
from django.contrib.auth.models import User


class ArbitrationCase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('in_progress', 'В процессе'),
        ('resolved', 'Решено'),
        ('rejected', 'Отклонено'),
    ]

    advertiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='arbitration_advertiser')
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='arbitration_publisher')
    advertisement = models.ForeignKey('Advertisement', on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Арбитраж {self.id} - {self.status}"



class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ArbitrationComment(models.Model):
    case = models.ForeignKey(ArbitrationCase, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий {self.id} в Арбитраже {self.case.id}"
