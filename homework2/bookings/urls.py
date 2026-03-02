from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'seats', views.SeatViewSet, basename='seat')
router.register(r'bookings', views.BookingViewSet, basename='booking')

urlpatterns = [
    path('api/', include(router.urls)),
    path('movies/', views.movie_list, name='movie_list'),
    path('book/<int:movie_id>/', views.seat_booking, name='seat_booking'),
    path('history/', views.booking_history, name='booking_history'),
]
