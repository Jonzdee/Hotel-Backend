from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
class Hotel(models.Model):
    id = models.BigAutoField(primary_key=True)
    hotelName = models.CharField(max_length=255)
    hotelAddress = models.CharField(max_length=255)
    hotelPhone = models.CharField(max_length=20)
    hotelEmail = models.EmailField(max_length=255)
    def __str__(self):
        return f'Id: {self.id}'
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=255)
    numberOfRooms = models.IntegerField()
    pricePerDay = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    asset1 = models.URLField(blank=True, null=True)
    asset2 = models.URLField(blank=True, null=True)
    asset3 = models.URLField(blank=True, null=True)
    asset4 = models.URLField(blank=True, null=True)
    asset5 = models.URLField(blank=True, null=True)
    def __str__(self):
        return f'Id: {self.id}'
class Guest(models.Model):
    id = models.BigAutoField(primary_key=True)
    guestName = models.CharField(max_length=255)
    guestEmail = models.EmailField()
    guestPhone = models.CharField(max_length=20)
    def __str__(self):
        return f'Id: {self.id}'
class Booking(models.Model):
    id = models.BigAutoField(primary_key=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    checkInDate = models.DateField()
    checkOutDate = models.DateField()
    totalAmount = models.DecimalField(max_digits=25, decimal_places=2, null=True, blank=True)
    isConfirmed = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)
    isCancelled = models.BooleanField(default=False)
    isRefund = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False, editable=False)
    payment_mail_sent = models.BooleanField(default=False, editable=False)
    cancellation_mail_sent = models.BooleanField(default=False, editable=False)
    refund_mail_sent = models.BooleanField(default=False, editable=False)
    def save(self, *args, **kwargs):
        if self.isRefund and not self.isCancelled:
            raise ValueError("Refund cannot be processed unless the booking is cancelled.")            
        if not self.pk or self.checkInDate != self.__class__.objects.get(pk=self.pk).checkInDate or self.checkOutDate != self.__class__.objects.get(pk=self.pk).checkOutDate or self.category != self.__class__.objects.get(pk=self.pk).category:
            if self.checkInDate < timezone.localdate():
                raise ValueError("Cannot book for past dates")
            if self.checkInDate > self.checkOutDate:
                raise ValueError("Check-in date must be before check-out date")
            self.totalAmount = (self.category.pricePerDay * ((self.checkOutDate - self.checkInDate).days + 1))
            overlapping_bookings = Booking.objects.filter(
                Q(checkInDate__lte=self.checkOutDate) &
                Q(checkOutDate__gte=self.checkInDate) &
                Q(category=self.category) &
                Q(isConfirmed=True) &
                Q(isPaid=True)
            ).count()
            if overlapping_bookings >= self.category.numberOfRooms:
                self.isConfirmed = False
            else:
                self.isConfirmed = True
        super().save(*args, **kwargs)
    def __str__(self):
        return f'Booking ID: {self.id}'
    def send_confirmation_email(self):
        subject = f'Booking Confirmation at {self.category.hotel.hotelName}'
        message = f'Dear {self.guest.guestName}\n\nWe are delighted to confirm your booking with {self.category.hotel.hotelName}\n\nHere are the details of your reservation:\n\nBooking Id: {self.id}\nDate: {self.checkInDate} to {self.checkOutDate}\nLocation: {self.category.hotel.hotelAddress}\n\nIf you have any special requests or need to make any changes, please let us know by replying to this {self.category.hotel.hotelEmail} or contacting us at {self.category.hotel.hotelPhone}\n\nWe look forward to providing you with an exceptional experience. Thank you for choosing {self.category.hotel.hotelName}\n\nBest regards,\n\nD&G Hotels\nCustomer Service\n{self.category.hotel.hotelEmail}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.guest.guestEmail]
        send_mail(subject, message, from_email, recipient_list)
    def send_rejection_email(self):
        subject = f'Booking Request Update at {self.category.hotel.hotelName}'
        message = f'Dear {self.guest.guestName},\n\nThank you for your interest in {self.category.hotel.hotelName}.\n\nWe regret to inform you that we are unable to accommodate your booking request on {self.checkInDate} to {self.checkOutDate} due to [brief reason, e.g., availability constraints, scheduling conflicts].\n\nWe understand this may be disappointing, and we apologize for any inconvenience this may cause. We would be happy to assist you with alternative dates or services if that would be helpful. Please let us know if you would like to explore other options or if there is anything else we can do for you.\n\nThank you for considering {self.category.hotel.hotelName}, and we hope to have the opportunity to serve you in the future.\n\nBest regards,\n\nD&G Hotels\nCustomer Service\n{self.category.hotel.hotelEmail}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.guest.guestEmail]
        send_mail(subject, message, from_email, recipient_list)
    def send_paymentreceived_email(self):
        subject = f'Payment Received and Booking Update'
        message = f'Dear {self.guest.guestName},\n\nThank you for your recent payment. We are pleased to confirm that we have successfully received your payment of {self.totalAmount} for your booking Id: {self.id} with {self.category.hotel.hotelName}.\n\nHere are the updated details of your booking:\nDate: From {self.checkInDate} to {self.checkOutDate}.\nLocation: {self.category.hotel.hotelAddress}.\n\nYour reservation is now fully confirmed.\n\nIf you have any questions or need further assistance, please do not hesitate to contact us at {self.category.hotel.hotelPhone} or {self.category.hotel.hotelEmail}.\n\nThank you once again for choosing {self.category.hotel.hotelName}. We look forward to serving you!\n\nBest regards,\n\nD&G Hotels\nCustomer Service \n{self.category.hotel.hotelEmail}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.guest.guestEmail]
        send_mail(subject, message, from_email, recipient_list)
    def send_cancellation_email(self):
        subject = f'Cancellation Request Received'
        message = f'Dear {self.guest.guestName},\n\nThank you for reaching out regarding your booking with {self.category.hotel.hotelName}.\n\n\nWe have received your request to cancel your reservation on {timezone.localdate()}.\n\nIf you have any further questions or need assistance with rescheduling, please let us know. We are here to help and ensure the process is as smooth as possible for you.\n\nThank you for your understanding, and we hope to have the opportunity to serve you in the future.\n\nBest regards,\n\nD&G Hotels\nCustomer Service \n{self.category.hotel.hotelEmail}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.guest.guestEmail]
        send_mail(subject, message, from_email, recipient_list)
    def send_refundprocessed_email(self):
        subject = f'Refund Processed for Your Cancellation'
        message = f"Dear {self.guest.guestName}\n\nWe are writing to inform you that your refund for the canceled booking at {self.category.hotel.hotelName} on {timezone.localdate()} has been successfully processed.\n\nYou should see the funds reflected in your account within [timeframe, e.g., 3-5 business days], depending on your bank or payment provider.\n\nIf you have any questions about the refund or need further assistance, please don't hesitate to reach out to us at {self.category.hotel.hotelEmail} or {self.category.hotel.hotelPhone}.\n\nThank you for your understanding, and we hope to have the pleasure of serving you in the future.\n\nBest regards,\n\nD&G Hotels\nCustomer Service \n{self.category.hotel.hotelEmail}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.guest.guestEmail]
        send_mail(subject, message, from_email, recipient_list)
class BookingCheck(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    checkInDate = models.DateField()
    checkOutDate = models.DateField()
    def is_available(self):
        if self.checkInDate < timezone.localdate():
            raise ValueError("Cannot book for past dates")
        if self.checkInDate > self.checkOutDate:
            raise ValueError("Check-in date must be before check-out date")
        overlapping_bookings = Booking.objects.filter(
            Q(checkInDate__lte=self.checkOutDate) &
            Q(checkOutDate__gte=self.checkInDate) &
            Q(category=self.category) &
            Q(isConfirmed=True) &
            Q(isPaid=True)
        ).count()
        return overlapping_bookings < self.category.numberOfRooms
    def save(self, *args, **kwargs):
        if not self.is_available():
            raise ValueError("The room is not available for the selected dates.")
@receiver(post_save, sender=Booking)
def send_booking_emails(sender, instance, created, **kwargs):
    if created:
        if instance.isConfirmed and not instance.email_sent:
            instance.send_confirmation_email()
        elif not instance.isConfirmed and not instance.email_sent:
            instance.send_rejection_email()
        instance.email_sent = True
        instance.save(update_fields=['email_sent'])
    else:
        if instance.isPaid and not instance.payment_mail_sent:
            instance.send_paymentreceived_email()
            instance.payment_mail_sent = True
            instance.save(update_fields=['payment_mail_sent'])
        
        elif instance.isCancelled and not instance.cancellation_mail_sent:
            instance.send_cancellation_email()
            instance.cancellation_mail_sent = True
            instance.save(update_fields=['cancellation_mail_sent'])
        elif instance.isRefund and not instance.refund_mail_sent and instance.isCancelled and instance.cancellation_mail_sent:
            instance.send_refundprocessed_email()
            instance.refund_mail_sent = True
            instance.save(update_fields=['refund_mail_sent'])