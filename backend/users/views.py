from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .tasks import send_verification_email 
from .tasks import send_registration_link
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

import logging
logger = logging.getLogger(__name__)

class RegisterAdminView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()  
        first_name = request.data.get('first_name', '').strip()
        last_name = request.data.get('last_name', '').strip()
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not email or not first_name or not last_name or not password:
            return Response({"error": "Tous les champs sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({"error": "Les mots de passe ne correspondent pas."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Cet email est déjà enregistré."}, status=status.HTTP_400_BAD_REQUEST)

        verification_code = str(random.randint(100000, 999999))

        try:
            user = User.objects.create_user(  
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,  
                role="admin",
                is_active=False,
                verification_code=verification_code
            )
            user.set_password(password) 
            user.save()

            logger.info(f"Admin créé : {email}, en attente de vérification.")

           
            send_verification_email.delay(email, verification_code)

            return Response(
                {"message": "Admin enregistré avec succès. Vérifiez votre email pour le code de vérification."},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.error(f"Erreur lors de la création de l'admin : {str(e)}")
            return Response({"error": "Une erreur s'est produite lors de l'inscription."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                        



class RegisterUserView(APIView):
    """
    Permet à un admin ou un installateur d'ajouter un utilisateur.
    L'utilisateur reçoit un email avec un lien pour compléter son inscription.
    """
    permission_classes = [permissions.IsAuthenticated]  

    def post(self, request):
        email = request.data.get('email')
        role = request.data.get('role')

        
        if role not in ['installateur', 'technicien', 'client']:
            return Response({"error": "Rôle invalide."}, status=status.HTTP_400_BAD_REQUEST)

        
        if request.user.role == 'installateur' and role == 'admin':
            return Response({"error": "Un installateur ne peut pas ajouter un admin."}, status=status.HTTP_403_FORBIDDEN)

        
        if User.objects.filter(email=email).exists():
            return Response({"error": "Cet email est déjà enregistré."}, status=status.HTTP_400_BAD_REQUEST)

      
        registration_token = str(uuid.uuid4())

        
        user = User.objects.create(
            email=email,
            role=role,
            username=email,
            is_active=False
        )
        user.set_password(registration_token)  
        user.save()

       
        FRONTEND_URL = "http://localhost:5173/complete-registration"
        registration_link = f"{FRONTEND_URL}?token={registration_token}&email={email}"
        send_registration_link.delay(email, registration_link)

        return Response({"message": "Utilisateur ajouté. Un email a été envoyé pour compléter l'inscription."}, status=status.HTTP_201_CREATED)


class CompleteRegistrationView(APIView):
    """
    Permet à un utilisateur de finaliser son inscription avec un mot de passe sécurisé.
    """
    permission_classes = [permissions.AllowAny]  

    def post(self, request):
        email = request.data.get('email')
        token = request.data.get('token')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password != confirm_password:
            return Response({"error": "Les mots de passe ne correspondent pas."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            if user.check_password(token):  
                user.set_password(password)
                user.is_active = True
                user.save()
                return Response({"message": "Inscription complétée avec succès."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user = request.user  
        return Response({
            "email": user.email,
            "first_name": user.first_name if user.first_name else "Non défini",
            "last_name": user.last_name if user.last_name else "Non défini",
            "role": user.role
        }, status=status.HTTP_200_OK)

class VerifyAdminView(APIView):
    """
    Verify admin email with a code.
    """
    permission_classes = [permissions.AllowAny]  

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = User.objects.get(email=email, role='admin')
            if user.verification_code == code:
                user.is_active = True
                user.verification_code = ""  
                user.save()
                return Response({"detail": "Account verified successfully. You can now log in."},
                                status=status.HTTP_200_OK)
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Admin not found."}, status=status.HTTP_404_NOT_FOUND)



class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        identifier = request.data.get("identifier")  
        password = request.data.get("password")

        if not identifier or not password:
            return Response({"error": "L'identifiant et le mot de passe sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        
        user = User.objects.filter(email=identifier).first() or User.objects.filter(username=identifier).first()

        if user is None:
            return Response({"error": "Identifiants invalides."}, status=status.HTTP_400_BAD_REQUEST)

       
        if not user.check_password(password):
            return Response({"error": "Identifiants invalides."}, status=status.HTTP_400_BAD_REQUEST)

        
        if not user.is_active:
            return Response({"error": "Votre compte est inactif. Veuillez vérifier votre email."}, status=status.HTTP_403_FORBIDDEN)

       
        user = authenticate(username=user.username, password=password)

        if user is None:
            return Response({"error": "Identifiants invalides."}, status=status.HTTP_400_BAD_REQUEST)

        
        refresh = RefreshToken.for_user(user)
        role_redirects = {
            "admin": "/",
            "installateur": "/",
            "technicien": "/",
            "client": "/",
        }
        redirect_url = role_redirects.get(user.role, "/")  

        
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            "redirect_url": redirect_url  
        }, status=status.HTTP_200_OK)






class UpdateProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        print("Utilisateur connecté :", self.request.user)
        return self.request.user  

    def update(self, request, *args, **kwargs):
        """
        Gère la mise à jour du profil et du mot de passe.
        """
        user = self.get_object()
        print("Données reçues pour mise à jour :", request.data)  

        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            print("Utilisateur mis à jour :", user.first_name, user.last_name)  
            return Response({"message": "Profil mis à jour avec succès.", "user": serializer.data})

        print("Erreurs de validation :", serializer.errors) 
        return Response(serializer.errors, status=400)
