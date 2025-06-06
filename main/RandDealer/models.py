from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import datetime

class Cars(models.Model):
    id = models.AutoField(primary_key=True)
    MAKER_CHOICES = [
        ('toyota', 'Toyota'),
        ('honda', 'Honda'),
        ('ford', 'Ford'),
        ('chevrolet', 'Chevrolet'),
        ('bmw', 'BMW'),
        ('audi', 'Audi'),
        ('mercedes', 'Mercedes-Benz'),
        ('nissan', 'Nissan'),
        ('volkswagen', 'Volkswagen'),
        ('hyundai', 'Hyundai'),
        ('kia', 'Kia'),
        ('mazda', 'Mazda'),
        ('subaru', 'Subaru'),
        ('lexus', 'Lexus'),
        ('infiniti', 'Infiniti'),
        ('acura', 'Acura'),
        ('mitsubishi', 'Mitsubishi'),
        ('porsche', 'Porsche'),
        ('jaguar', 'Jaguar'),
        ('land_rover', 'Land Rover'),
        ('fiat', 'Fiat'),
        ('alfa_romeo', 'Alfa Romeo'),
        ('volvo', 'Volvo'),
        ('tesla', 'Tesla'),
    ]

    YEAR_CHOICES = [(year, year) for year in range(datetime.now().year, 1980, -1)]

    CONDITION_CHOICES = [
        ('NEW', 'New'),
        ('USED_EXCELLENT', 'Used - Excellent'),
        ('USED_GOOD', 'Used - Good'),
        ('USED_BAD', 'Used - Bad'),
        ('USED', 'Used'),
    ]

    maker = models.CharField(max_length=50, choices=MAKER_CHOICES)
    model = models.CharField(max_length=50)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.now().year)
    mileage = models.IntegerField()
    price = models.IntegerField()
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='USED_BAD')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')

    def __str__(self):
        return f"{self.year} {self.maker} {self.model}"

class CarImage(models.Model):
    car = models.ForeignKey(Cars, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car}"

@receiver(post_delete, sender=CarImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
    
#custom User model to add e-mail token
class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        expiration = self.created_at + timezone.timedelta(days=1)
        return timezone.now() > expiration
    
    def __str__(self):
        return f"{self.user} {self.is_verified} {self.token} {self.created_at}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profilepic/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        try:
            this = UserProfile.objects.get(id=self.id)
            if this.profile_picture != self.profile_picture and this.profile_picture:
                if os.path.isfile(this.profile_picture.path):
                    os.remove(this.profile_picture.path)
        except UserProfile.DoesNotExist:
            pass
        super(UserProfile, self).save(*args, **kwargs)


class NewsletterSub(models.Model):
    email = models.EmailField()

    def __str__(self):
        return f'Email: {self.email}'