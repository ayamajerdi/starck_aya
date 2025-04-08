from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import ProductionConsommation
from .serializers import ProductionConsommationSerializer
from installations.models import Installation
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from users.permissions import IsAdminOrInstallateur
from rest_framework.permissions import IsAuthenticated


class AjouterDonneesView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrInstallateur]

    def post(self, request):
        serializer = ProductionConsommationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Donnée ajoutée avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListeProductionView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrInstallateur]

    def get(self, request):
        installation_id = request.query_params.get('installation_id')
        if not installation_id:
            return Response({"error": "installation_id requis"}, status=400)
        
        donnees = ProductionConsommation.objects.filter(installation__id=installation_id)
        serializer = ProductionConsommationSerializer(donnees, many=True)
        return Response(serializer.data, status=200)

class StatistiquesGlobalesView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrInstallateur]

    def get(self, request):
        base_qs = ProductionConsommation.objects.all()

        jour = base_qs.filter(horodatage__date=timezone.now().date()).aggregate(total=Sum('energie_produite_kwh'))['total'] or 0
        mois = base_qs.filter(horodatage__year=timezone.now().year, horodatage__month=timezone.now().month).aggregate(total=Sum('energie_produite_kwh'))['total'] or 0
        annee = base_qs.filter(horodatage__year=timezone.now().year).aggregate(total=Sum('energie_produite_kwh'))['total'] or 0
        totale = base_qs.aggregate(total=Sum('energie_produite_kwh'))['total'] or 0
        puissance = base_qs.aggregate(max=Sum('puissance_maximale_kw'))['max'] or 0

        return Response({
            "production_journaliere": jour,
            "production_mensuelle": mois,
            "production_annuelle": annee,
            "production_totale": totale,
            "puissance_totale": puissance
        }, status=200)


class StatistiquesProductionView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrInstallateur]

    def get(self, request, installation_id):
        today = timezone.now().date()
        year = today.year
        month = today.month

        base_qs = ProductionConsommation.objects.filter(installation_id=installation_id)

        jour = base_qs.filter(horodatage__date=today).aggregate(total=Sum('energie_produite_kwh'))['total'] or 0
        mois = base_qs.filter(horodatage__year=year, horodatage__month=month).aggregate(total=Sum('energie_produite_kwh'))['total'] or 0
        annee = base_qs.filter(horodatage__year=year).aggregate(total=Sum('energie_produite_kwh'))['total'] or 0
        totale = base_qs.aggregate(total=Sum('energie_produite_kwh'))['total'] or 0
        puissance = base_qs.aggregate(max=Sum('puissance_maximale_kw'))['max'] or 0

        return Response({
            "production_journaliere": jour,
            "production_mensuelle": mois,
            "production_annuelle": annee,
            "production_totale": totale,
            "puissance_totale": puissance
        }, status=200)