from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (UserProfileDetailAPIView, CityListAPIView, CityDetailSerializer,
                    PropertyListAPIView, PropertyDetailAPIView,
                    PropertyImageViewSet, BookingCreateAPIView, BookingUpdateAPIView,
                    BookingCancelAPIView,
                    ReviewCreateAPIView, RegisterView, LogoutView, CityDetailAPIView)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

router = DefaultRouter()
router.register(r'property_image', PropertyImageViewSet)


urlpatterns = [
    path('properties/', PropertyListAPIView.as_view(), name='property_list'),
    path('properties/<int:pk>/', PropertyDetailAPIView.as_view(), name='property_detail'),
    path('bookings/', BookingCreateAPIView.as_view(), name='booking_create'),
    path('bookings/<int:pk>/', BookingUpdateAPIView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/cancel/', BookingCancelAPIView.as_view(), name='booking_cancel'),
    path('city/', CityListAPIView.as_view(), name='city_list'),
    path('city/<int:pk>/', CityDetailAPIView.as_view(), name='city_detail'),
    path('reviews/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('auth/user/',UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('allauth.urls')),
    path('', include(router.urls)),

]