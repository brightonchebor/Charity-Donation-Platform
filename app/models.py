from django.db import models
from django.contrib.auth.models import User

    
class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    def __str__(self):
        return f'{self.name} by {self.owner}'
    
class Campaign(models.Model):
    choices = [
        ('Ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ]
    title = models.CharField(max_length=255)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_donations = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=choices, default='Ongoing')
    goals_and_plans = models.TextField(blank=True, null=True, help_text="Describe your organization's goals, expectations, and how the funds will be used.")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='campaigns')
    image = models.ImageField(upload_to='images')

    @property
    def progress_percentage(self):
        if self.goal_amount > 0:
            return int((self.total_donations / self.goal_amount) * 100)
        return 0

    def __str__(self):
        return f'{self.title} of {self.organization}'

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    donor_phone = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='approved')
    transaction_time = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='transactions')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f'{self.amount} donated by {self.donor_phone} to {self.organization.name}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.campaign.total_donations = sum(transaction.amount for transaction in self.campaign.transactions.all())
        self.campaign.save()


class ContactUs(models.Model):
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f'{self.email} - {self.phone}'