from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'guests', GuestViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'availability', BookingCheckViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('filter/', show_filter_form, name='show_filter_form'),
]
