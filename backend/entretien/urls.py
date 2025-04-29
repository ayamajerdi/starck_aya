from django.urls import path
from .views import (
    EntretienListCreateAPIView,
    EntretienDetailAPIView,
    EntretienCalendarAPIView,
    EntretienStatistiquesView,
    RappelEntretienAPIView,
    MesEntretiensAPIView, 
    MesEntretiensInstallateurAPIView,
    EntretienCalendarInstallateurAPIView
)

urlpatterns = [
    path('entretiens/', EntretienListCreateAPIView.as_view(), name='entretien-list-create'),
    path('entretiens/<int:pk>/', EntretienDetailAPIView.as_view(), name='entretien-detail'),
    path('entretiens/calendar/', EntretienCalendarAPIView.as_view(), name='entretien-calendar'),
    path("entretien/statistiques/", EntretienStatistiquesView.as_view(), name="entretien-statistiques"),
    path('entretiens/<int:entretien_id>/rappel/', RappelEntretienAPIView.as_view(), name='ajouter-rappel'),
    path('entretiens/mes-entretiens/', MesEntretiensAPIView.as_view(), name='mes-entretiens'),

    path('entretiens/mes-entretiens-installateur/', MesEntretiensInstallateurAPIView.as_view(), name='mes-entretiens-installateur'),  # ➡️ ici
path('entretiens/calendar-installateur/', EntretienCalendarInstallateurAPIView.as_view(), name='entretien-calendar-installateur'),

]


