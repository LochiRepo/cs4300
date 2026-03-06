from rest_framework import viewsets, permissions
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ModelViewSet):
    serializer_class = SeatSerializer
    def get_queryset(self):
        queryset = Seat.objects.all()
        available = self.request.query_params.get('available')
        if available:
            queryset = queryset.filter(bookingStatus='available')
        return queryset

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Booking.objects.filter(userReference=self.request.user)
    def perform_create(self, serializer):
        serializer.save(userReference=self.request.user)

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})

def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    booked_seat_numbers = Booking.objects.filter(
        movieReference=movie
    ).values_list('seatReference__seatNumber', flat=True)

    now = timezone.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    next_showing = next_hour.strftime('%I:%M %p')

    if request.method == 'POST':
        seat_ids = request.POST.get('seats', '')
        print(f"POST received - seats: {seat_ids}, user: {request.user}, auth: {request.user.is_authenticated}")
        if seat_ids and request.user.is_authenticated:
            for seat_number in seat_ids.split(','):
                seat_number = seat_number.strip()
                if seat_number:
                    seat, created = Seat.objects.get_or_create(
                        seatNumber=seat_number,
                        defaults={'bookingStatus': 'available'}
                    )
                    # Force status to available so clean() doesn't block it
                    if seat.bookingStatus != 'available':
                        Seat.objects.filter(seatNumber=seat_number).update(bookingStatus='available')
                        seat.refresh_from_db()
                    try:
                        Booking.objects.get_or_create(
                            movieReference=movie,
                            seatReference=seat,
                            defaults={'userReference': request.user}
                        )
                        print(f"Booked seat {seat_number}")
                    except Exception as e:
                        print(f"Error on {seat_number}: {e}")
        return redirect('booking_history')

    return render(request, 'bookings/seat_booking.html', {
        'movie': movie,
        'booked_seat_numbers': list(booked_seat_numbers),
        'next_showing': next_showing,
    })

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(userReference=request.user)
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})