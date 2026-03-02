from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Movie(models.Model):
    movieTitle = models.CharField(max_length=200)
    movieDescription = models.TextField()
    releaseDate = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.movieTitle


class Seat(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('reserved', 'Reserved'),
    ]

    seatNumber = models.CharField(max_length=10)
    bookingStatus = models.CharField(
        max_length=10,
        choices=BOOKING_STATUS_CHOICES,
        default='available'
    )

    def __str__(self):
        return f"Seat {self.seatNumber} ({self.bookingStatus})"


class Booking(models.Model):
    movieReference = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='bookingRecords'
    )

    seatReference = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name='bookingRecords'
    )

    userReference = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookingRecords'
    )

    bookingDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movieReference', 'seatReference')

    def clean(self):
        if self.seatReference.bookingStatus == 'booked':
            raise ValidationError("This seat is already booked.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        self.seatReference.bookingStatus = 'booked'
        self.seatReference.save()

    def __str__(self):
        return (
            f"{self.userReference.username} - "
            f"{self.movieReference.movieTitle} - "
            f"Seat {self.seatReference.seatNumber}"
        )