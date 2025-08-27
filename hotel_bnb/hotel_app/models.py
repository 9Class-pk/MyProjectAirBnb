from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


class City(models.Model):
    city_name = models.CharField(max_length=24, unique=True, db_index=True)

    def __str__(self):
        return self.city_name


class UserProfile(AbstractUser):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    user_avatar = models.ImageField(upload_to='user_avatars/', blank=True)
    phone_number = PhoneNumberField(blank=True)
    ROLE_CHOICES = (
    ('guest', 'guest'),
    ('host', 'host')
    )
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='guest')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}, {self.role}'


class Service(models.Model):
    service_image = models.ImageField(upload_to='service_images')
    service_name = models.CharField(max_length=32)

    def __str__(self):
        return self.service_name


class Property(models.Model):
    title = models.TextField()
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True, related_name="properties")
    address = models.CharField(max_length=32)
    PROPERTY_CHOICES = (
    ('apartment', 'apartment'),
    ('house', 'house'),
    ('studio', 'studio')
    )
    property_type = models.CharField(max_length=32, choices=PROPERTY_CHOICES, default='apartment')
    RULES_CHOICES = (
    ('no_smoking', 'no_smoking'),
    ('pets_allowed', 'pets_allowed'),
    ('etc', 'etc')
    )
    rules = models.CharField(max_length=32, choices=RULES_CHOICES)
    max_guests = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    bedrooms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    bathrooms = models.FloatField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="properties")
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service = models.ManyToManyField(Service)

    def __str__(self):
        return f'{self.property_type}, {self.rules}, {self.bedrooms}, {self.bathrooms}, {self.title}, {self.city}'


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_images')
    property_image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f'{self.property}'



class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    STATUS_CHOICES = (
    ('pending', 'pending'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
    ('cancelled', 'cancelled')
    )
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.property}, {self.guest}'


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.property}, {self.guest}, {self.rating}'


class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.favorite}, {self.property}'


