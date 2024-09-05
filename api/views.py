from rest_framework import viewsets
from django.shortcuts import render
from .models import *
from .serializers import *
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
class BookingCheckViewSet(viewsets.ModelViewSet):
    queryset = BookingCheck.objects.all()
    serializer_class = BookingCheckSerializer
def show_filter_form(request):
    if request.method == 'POST':
        checkInDate = request.POST.get('checkInDate')
        checkOutDate = request.POST.get('checkOutDate')
        category = request.POST.get('category')
        isConfirmed = request.POST.get('isConfirmed')
        isPaid = request.POST.get('isPaid')
        isCancelled = request.POST.get('isCancelled')
        isRefund = request.POST.get('isRefund')
        filters = Q(checkInDate__lte=checkOutDate) & Q(checkOutDate__gte=checkInDate)
        if category != 'any':
            filters &= Q(category__categoryType__iexact=category)
        if isConfirmed.lower() != 'any':
            filters &= Q(isConfirmed=isConfirmed.lower() == 'true')
        if isPaid.lower() != 'any':
            filters &= Q(isPaid=isPaid.lower() == 'true')
        if isCancelled.lower() != 'any':
            filters &= Q(isCancelled=isCancelled.lower() == 'true')
        if isRefund.lower() != 'any':
            filters &= Q(isRefund=isRefund.lower() == 'true')
        filtered_bookings = Booking.objects.filter(filters)
        return render(request, 'filterResult.html', {'result': filtered_bookings} )
    return render(request, 'filterForm.html')