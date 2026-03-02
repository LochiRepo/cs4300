# Create your views here.
from rest_framework import viewsets, permissions
from django.shortcuts import render
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ModelViewSet):
    serializer_class = SeatSerializer

    def get_queryset(self):
        queryset = Seat.objects.all()
        available = self.request.query_params.get('available')
        if available:
            queryset = queryset.filter(seatBook=False)
        return queryset

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(bookUser=self.request.user)

    def perform_create(self, serializer):
        serializer.save(bookUser=self.request.user)

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})

def seat_booking(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    seats = Seat.objects.filter(seatMovie=movie)
    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})

def booking_history(request):
    bookings = Booking.objects.filter(bookUser=request.user)
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})