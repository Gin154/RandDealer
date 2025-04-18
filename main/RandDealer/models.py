from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User

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

    CONDITION_CHOICES = [
        ('NEW', 'New'),
        ('USED_EXCELLENT', 'Used - Excellent'),
        ('USED_GOOD', 'Used - Good'),
        ('USED_BAD', 'Used - Bad'),
        ('USED', 'Used'),
    ]

    maker = models.CharField(max_length=50, choices=MAKER_CHOICES)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='USED')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.maker} {self.model}"

class CarImage(models.Model):
    car = models.ForeignKey(Cars, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car}"
    
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
    

