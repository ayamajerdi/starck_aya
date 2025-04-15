from django.urls import path
from .views import (
    EntretienListCreateAPIView,
    EntretienDetailAPIView,
    EntretienCalendarAPIView
)

urlpatterns = [
    path('entretiens/', EntretienListCreateAPIView.as_view(), name='entretien-list-create'),
    path('entretiens/<int:pk>/', EntretienDetailAPIView.as_view(), name='entretien-detail'),
    path('entretiens/calendar/', EntretienCalendarAPIView.as_view(), name='entretien-calendar'),
]