from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    movieTitle = models.CharField(max_length=69, default='')
    movieDescription = models.TextField(default='')
    movieRelease = models.DateField(default='2000-01-01')
    movieDuration = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.movieTitle


class Seat(models.Model):
    seatMovie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seats')
    seatNumber = models.CharField(max_length=10, default='')
    seatBook = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seatMovie.movieTitle} - Seat {self.seatNumber}"


class Booking(models.Model):
    bookUser = models.ForeignKey(User, on_delete=models.CASCADE)
    bookMovie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    bookSeats = models.ManyToManyField(Seat)
    bookTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.bookUser.username} for {self.bookMovie.movieTitle}"
