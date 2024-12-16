from django.contrib.auth.models import User
from django.db import models

LETTERS = [(chr(i), chr(i)) for i in range(65, 91)]


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=7, default='#000000')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="Описание отсутствует")
    letter = models.CharField(max_length=1, choices=LETTERS, unique=True)
    category = models.ForeignKey('Category', related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Operator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    window_number = models.IntegerField()

    def __str__(self):
        return f'Operator {self.user.username} - Window {self.window_number}'


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('in_service', 'In Service'),
        ('served', 'Served'),
    ]

    number = models.CharField(max_length=10)
    issued_at = models.DateTimeField(auto_now_add=True)
    is_served = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    served_by = models.CharField(max_length=100, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Ticket {self.number} - {"Served" if self.is_served else "Waiting"}'

    class Meta:
        ordering = ['number']
