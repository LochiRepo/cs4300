import pytest
from django.test import Client
from django.contrib.auth.models import User
from bookings.models import Movie, Seat, Booking
from datetime import date
from unittest.mock import patch

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

# ── API HAPPY PATH ────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_api_movies_returns_200(client):
    response = client.get('/api/movies/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_api_movies_returns_json(client, movie):
    response = client.get('/api/movies/')
    data = response.json()
    assert isinstance(data, list)
    assert data[0]['movieTitle'] == 'Test Movie'

@pytest.mark.django_db
def test_api_seats_returns_200(client):
    response = client.get('/api/seats/')
    assert response.status_code == 200

# ── API EDGE CASES ────────────────────────────────────────────────────────────

@pytest.mark.django_db
def test_api_bookings_requires_auth(client):
    response = client.get('/api/bookings/')
    assert response.status_code == 403

@pytest.mark.django_db
def test_api_seats_available_filter(client):
    Seat.objects.create(seatNumber='A1', bookingStatus='available')
    Seat.objects.create(seatNumber='A2', bookingStatus='booked')
    response = client.get('/api/seats/?available=true')
    data = response.json()
    assert all(s['bookingStatus'] == 'available' for s in data)
