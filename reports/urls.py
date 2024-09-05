from django.urls import path
from .views import *
urlpatterns = [
    path('hotels/', download_hotel_report, name='download_hotel_report'),
    path('rooms/', download_room_report, name='download_room_report'),
    path('guests/', download_guest_report, name='download_guest_report'),
    path('bookings/', download_booking_report, name='download_booking_report'),
    path('', report_page, name='report_page'),
]