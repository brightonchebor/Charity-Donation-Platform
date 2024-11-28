from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_lenght=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    
class Campaign(models.Model):
    choices = [
        ('Ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ]
    title = models.CharField(max_length=255)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_donations = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=choices)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='campaigns')
    image = models.OneToOneField('UploadedImage')

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    donor_phone = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='approved')
    transaction_date = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='transactions')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='transactions')

class UploadedImage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploaded_images', on_delete=models.SET_NULL, null=True, blank=True)

    