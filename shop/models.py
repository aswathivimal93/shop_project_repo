from django.conf import settings
from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    total_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_consumers = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_shops')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_shops')
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class ShopUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    username=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    total_collection = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    related_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_users', null=True, default=None)
    def __str__(self):
        return self.username

class Consumer(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    total_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_payment_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='created_consumers')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='updated_consumers')
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    AMOUNT_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    consumer = models.OneToOneField('Consumer', on_delete=models.CASCADE)
    shop = models.OneToOneField('Shop', on_delete=models.CASCADE)
    type = models.CharField(max_length=6, choices=AMOUNT_CHOICES, default='credit')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='payments_created', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='payments_updated', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)

    # Additional fields specific to credit payments
    #credit_limit = models.DecimalField(max_digits=10, decimal_places=2)
    #remaining_credit = models.DecimalField(max_digits=10, decimal_places=2)
