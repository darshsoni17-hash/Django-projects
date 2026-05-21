from django.utils import timezone
from django.db import models

# Create your models here.

class chaivarity(models.Model):
    chai_TYPE_CHOICE = [
        ('ML', 'MASALA'),
        ('GR', 'GINGER'),
        ('KL', 'KIWI'),
        ('PL', 'PLAIN'),
        ('EL', 'ELACHI'),
    ]

    name = models.CharField(max_length=100)
    price = models.ImageField(upload_to='chais/')
    date_added = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2, choices=chai_TYPE_CHOICE)

    def __str__(self):
        return self.name