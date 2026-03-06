import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from bookings.models import Movie, Seat, Booking
from datetime import date


# ── FIXTURES ──────────────────────────────────────────────────────────────────

@pytest.fixture
def movie():
    return Movie.objects.create(
        movieTitle='Test Movie',
        movieDescription='A test movie description.',
        releaseDate=date(2024, 1, 1),
        duration=120
    )

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def available_seat():
    return Seat.objects.create(seatNumber='A1')

@pytest.fixture
def booked_seat():
    seat = Seat.objects.create(seatNumber='B1', bookingStatus='booked')
    return seat


# ── MOVIE TESTS ───────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_movie_creation(movie):
    assert movie.movieTitle == 'Test Movie'
    assert movie.duration == 120
    assert movie.releaseDate == date(2024, 1, 1)

@pytest.mark.django_db
def test_movie_str(movie):
    assert str(movie) == 'Test Movie'

@pytest.mark.django_db
def test_movie_description_saved(movie):
    assert movie.movieDescription == 'A test movie description.'


# ── SEAT TESTS ────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_seat_default_status():
    seat = Seat.objects.create(seatNumber='C1')
    assert seat.bookingStatus == 'available'

@pytest.mark.django_db
def test_seat_str(available_seat):
    assert 'A1' in str(available_seat)
    assert 'available' in str(available_seat)

@pytest.mark.django_db
def test_seat_can_be_booked(available_seat):
    available_seat.bookingStatus = 'booked'
    available_seat.save()
    assert Seat.objects.get(seatNumber='A1').bookingStatus == 'booked'

@pytest.mark.django_db
def test_seat_can_be_reserved(available_seat):
    available_seat.bookingStatus = 'reserved'
    available_seat.save()
    assert Seat.objects.get(seatNumber='A1').bookingStatus == 'reserved'


# ── BOOKING TESTS ─────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_booking_creation(movie, user, available_seat):
    booking = Booking.objects.create(
        movieReference=movie,
        seatReference=available_seat,
        userReference=user
    )
    assert booking.movieReference == movie
    assert booking.seatReference == available_seat
    assert booking.userReference == user

@pytest.mark.django_db
def test_booking_sets_seat_to_booked(movie, user, available_seat):
    Booking.objects.create(
        movieReference=movie,
        seatReference=available_seat,
        userReference=user
    )
    available_seat.refresh_from_db()
    assert available_seat.bookingStatus == 'booked'

@pytest.mark.django_db
def test_booking_str(movie, user, available_seat):
    booking = Booking.objects.create(
        movieReference=movie,
        seatReference=available_seat,
        userReference=user
    )
    assert 'testuser' in str(booking)
    assert 'Test Movie' in str(booking)
    assert 'A1' in str(booking)

@pytest.mark.django_db
def test_cannot_book_already_booked_seat(movie, user, booked_seat):
    with pytest.raises(ValidationError):
        Booking.objects.create(
            movieReference=movie,
            seatReference=booked_seat,
            userReference=user
        )

@pytest.mark.django_db
def test_unique_together_blocks_duplicate_booking(movie, user, available_seat):
    Booking.objects.create(
        movieReference=movie,
        seatReference=available_seat,
        userReference=user
    )
    available_seat.refresh_from_db()
    with pytest.raises(Exception):
        Booking.objects.create(
            movieReference=movie,
            seatReference=available_seat,
            userReference=user
        )

@pytest.mark.django_db
def test_booking_date_auto_set(movie, user, available_seat):
    booking = Booking.objects.create(
        movieReference=movie,
        seatReference=available_seat,
        userReference=user
    )
    assert booking.bookingDate is not None


# ── DEFENSIVE/VALIDATION TESTS ────────────────────────────────────────────────

@pytest.mark.django_db
def test_invalid_seat_status_rejected():
    seat = Seat(seatNumber='D1', bookingStatus='invalid_status')
    with pytest.raises(ValidationError):
        seat.full_clean()

@pytest.mark.django_db
def test_movie_title_max_length():
    long_title = 'A' * 201
    movie = Movie(
        movieTitle=long_title,
        movieDescription='desc',
        releaseDate=date(2024, 1, 1),
        duration=120
    )
    with pytest.raises(ValidationError):
        movie.full_clean()

@pytest.mark.django_db
def test_seat_number_max_length():
    seat = Seat(seatNumber='A' * 11)
    with pytest.raises(ValidationError):
        seat.full_clean()


# ── PARAMETRIZED SEAT VALIDATION ──────────────────────────────────────────────

@pytest.mark.parametrize("bad_status", [
    'invalid', 'BOOKED', 'Available', '', 'reserved123', 'null'
])
@pytest.mark.django_db
def test_invalid_seat_statuses_rejected(bad_status):
    seat = Seat(seatNumber='A1', bookingStatus=bad_status)
    with pytest.raises(ValidationError):
        seat.full_clean()

@pytest.mark.parametrize("valid_status", ['available', 'booked', 'reserved'])
@pytest.mark.django_db
def test_valid_seat_statuses_accepted(valid_status):
    seat = Seat(seatNumber='A1', bookingStatus=valid_status)
    seat.full_clean()  # Should not raise

@pytest.mark.parametrize("seat_number", [
    'A1', 'H20', 'E15', 'B10', 'D5'
])
@pytest.mark.django_db
def test_valid_seat_numbers(seat_number):
    seat = Seat.objects.create(seatNumber=seat_number)
    assert seat.seatNumber == seat_number

@pytest.mark.parametrize("duration", [1, 60, 120, 228, 360])
@pytest.mark.django_db
def test_movie_various_durations(duration):
    movie = Movie.objects.create(
        movieTitle=f'Test Movie {duration}',
        movieDescription='desc',
        releaseDate=date(2024, 1, 1),
        duration=duration
    )
    assert movie.duration == duration