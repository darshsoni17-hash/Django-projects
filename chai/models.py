from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.

class chaivarity(models.Model):
    chai_TYPE_CHOICE = [
        ('ML', 'MASALA'),
        ('GR', 'GINGER'),
        ('KL', 'KIWI'),
        ('PL', 'PLAIN'),
        ('EL', 'ELACHI'),
        ('Lm', 'LEMON'),
        ('IC', 'ICE'),
        ('GT', 'GREEN'),
        ('SF', 'Saffron'),
        ('BL', 'BLACK'),
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='chai/', null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2, choices=chai_TYPE_CHOICE)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.name

# one to many

class chaireview(models.Model):
    chai = models.ForeignKey(chaivarity, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} review for {self.chai.name}'
    
# many to many

class store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    chai_varities = models.ManyToManyField(chaivarity, related_name='stores')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    

    def gst_amount(self):
        return round(self.price * Decimal('0.18'), 2)

    def total_with_gst(self):
        return round(self.price + self.gst_amount(), 2)
    
# one to one

class chaicertificate(models.Model):
    chai = models.OneToOneField(chaivarity, on_delete=models.CASCADE, related_name='certificate')
    certificate_number = models.CharField(max_length=100)
    issued_date = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()

    def __str__(self):
        return f'Certificate for {self.chai.name}'  
    
class storereview(models.Model):
    store = models.ForeignKey(store, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} review for {self.store.name}'    

class Cart(models.Model):
    session_key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Cart {self.id}'

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

    def total_gst(self):
        return round(self.total_price() * Decimal('0.18'), 2)

    def grand_total(self):
        return round(self.total_price() + self.total_gst(), 2)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    chai = models.ForeignKey(chaivarity, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.chai.name}'

    def subtotal(self):
        return self.chai.price * self.quantity

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI'),
        ('CARD', 'Credit/Debit Card'),
    ]

    session_key = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    gst = models.DecimalField(max_digits=8, decimal_places=2)
    grand_total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Order {self.id} - {self.payment_method}'    