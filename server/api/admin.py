from django.contrib import admin
from .models import *
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotelName', 'hotelAddress', 'hotelPhone', 'hotelEmail')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'categoryType', 'numberOfRooms', 'pricePerDay', 'capacity', 'description', 'asset1', 'asset2', 'asset3', 'asset4', 'asset5')
    search_fields = ('id', 'hotel', 'categoryType', 'numberOfRooms', 'pricePerDay', 'capacity', 'description', 'asset1', 'asset2', 'asset3', 'asset4', 'asset5')
    list_filter = ('id', 'hotel', 'categoryType', 'numberOfRooms', 'pricePerDay', 'capacity', 'description', 'asset1', 'asset2', 'asset3', 'asset4', 'asset5')
class GuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'guestName', 'guestEmail', 'guestPhone')
    search_fields = ('id', 'guestName', 'guestEmail', 'guestPhone')
    list_filter = ('id', 'guestName', 'guestEmail', 'guestPhone')
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'category', 'checkInDate', 'checkOutDate', 'totalAmount', 'isConfirmed', 'isPaid', 'isCancelled', 'isRefund')
    search_fields = ('guest__guestName', 'guest__guestEmail', 'guest__guestPhone', 'category__categoryType', 'category__hotel__hotelName', 'checkInDate', 'checkOutDate',)
    list_filter = ('isConfirmed', 'isPaid', 'isCancelled', 'isRefund', 'category__categoryType', 'guest__guestEmail', 'checkInDate', 'checkOutDate',)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingCheck)
