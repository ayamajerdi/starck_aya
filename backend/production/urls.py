# urls.py
from django.urls import path
from .views import AjouterDonneesView, StatistiquesProductionView, ListeProductionView, StatistiquesGlobalesView

urlpatterns = [
path('ajouter_prod/', AjouterDonneesView.as_view(), name='ajouter-donnees'),
path('list_prod/', ListeProductionView.as_view(), name='ajouter-donnees'),
path('statistiques/<int:installation_id>/', StatistiquesProductionView.as_view(), name='statistiques-production'),
path('statistiques/globales/', StatistiquesGlobalesView.as_view(), name='statistiques_globales'),

]