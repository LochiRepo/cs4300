import pytest
from django.test import Client
from django.contrib.auth.models import User
from bookings.models import Movie, Seat, Booking
from datetime import date

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass123')

@pytest.fixture
def movie(db):
    return Movie.objects.create(
        movieTitle='Test Movie',
        movieDescription='desc',
        releaseDate=date(2024, 1, 1),
        duration=120
    )

# ── HAPPY PATH ────────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_movie_list_returns_200(client):
    response = client.get('/movies/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_seat_booking_page_returns_200(client, movie):
    response = client.get(f'/book/{movie.id}/')
    assert response.status_code == 200

# ── AUTHENTICATION EDGE CASES ─────────────────────────────────────────────────

@pytest.mark.django_db
def test_history_redirects_when_not_logged_in(client):
    response = client.get('/history/')
    assert response.status_code == 302
    assert '/admin/login/' in response.url

@pytest.mark.django_db
def test_history_accessible_when_logged_in(client, user):
    client.login(username='testuser', password='testpass123')
    response = client.get('/history/')
    assert response.status_code == 200

# ── BOUNDARY/EDGE CASES ───────────────────────────────────────────────────────

@pytest.mark.django_db
def test_booking_nonexistent_movie(client, user):
    client.login(username='testuser', password='testpass123')
    response = client.get('/book/99999/')
    assert response.status_code == 404

@pytest.mark.parametrize("bad_seat_input", [
    '',
    '   ',
    'Z99,AA1,!!',
    'A1' * 500,
    '<script>alert(1)</script>',
    "'; DROP TABLE bookings;--",
])
@pytest.mark.django_db
def test_booking_bad_seat_inputs_dont_crash(client, user, movie, bad_seat_input):
    client.login(username='testuser', password='testpass123')
    response = client.post(f'/book/{movie.id}/', {'seats': bad_seat_input})
    assert response.status_code in [200, 302]

@pytest.mark.django_db
def test_booking_post_without_seats_field(client, user, movie):
    client.login(username='testuser', password='testpass123')
    response = client.post(f'/book/{movie.id}/', {})
    assert response.status_code in [200, 302]

@pytest.mark.django_db
def test_booking_unauthenticated_post_rejected(client, movie):
    response = client.post(f'/book/{movie.id}/', {'seats': 'A1'})
    assert Booking.objects.count() == 0

# ── RETURN TYPE VERIFICATION ──────────────────────────────────────────────────

@pytest.mark.django_db
def test_movie_list_context_contains_movies(client, movie):
    response = client.get('/movies/')
    assert 'movies' in response.context
    assert len(response.context['movies']) >= 1

@pytest.mark.django_db
def test_seat_booking_context_contains_booked_seats(client, movie):
    response = client.get(f'/book/{movie.id}/')
    assert 'booked_seat_numbers' in response.context
    assert isinstance(response.context['booked_seat_numbers'], list)