from django.contrib.auth.password_validation import validate_password
from rest_framework.fields import SerializerMethodField
from .models import (City, UserProfile, Property, PropertyImage, Booking, Review, Service, Favorite, FavoriteItem)
from rest_framework import serializers
from django.db.models import Avg, Count
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields ='__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices= UserProfile.ROLE_CHOICES)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'password2','role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = UserProfile.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'id': instance.id,
                'username': instance.username,
                'email': instance.email,
                'role': instance.role,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','first_name', 'last_name', 'role']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating',]


class PropertyListSerializer(serializers.ModelSerializer):
    average_rating = SerializerMethodField()
    class Meta:
        model = Property
        fields = ['title', 'city', 'price', 'average_rating']

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg is not None else None


class CityDetailSerializer(serializers.ModelSerializer):
    properties = PropertyListSerializer(many=True, read_only=True)
    class Meta:
        model = City
        fields = ['city_name', 'properties',]


class PropertyDetailSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(many=True, read_only=True)
    service_images = ServiceSerializer(many=True, read_only=True)
    owner = OwnerSerializer(read_only=True)
    city = CityDetailSerializer(read_only=True)
    reviews = ReviewSerializer(many=True ,read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_people = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['title', 'description', 'address', 'rules',
                  'max_guests', 'bedrooms', 'bathrooms', 'is_active',
                  'city', 'price', 'owner','service_images',
                  'reviews', 'average_rating', 'bookings', 'service', 'reviews_people']

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg is not None else None

    def get_reviews_people(self, obj):
        count = obj.reviews.aggregate(people=Count('id'))['people']
        return count


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = '__all__'





