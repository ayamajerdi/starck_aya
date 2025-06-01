"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from entretien.views import start_google_auth, google_auth_callback

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('installations/', include('installations.urls')),
    path('alarme/', include('alarme.urls')),
    path('notification/', include('notification.urls')),
    path('production/', include('production.urls')),
    path('intervention/', include('intervention.urls')),
    path('entretien/', include('entretien.urls')),
    path('reclamation/', include('reclamation.urls')),
    path('rapports/', include('rapports.urls')),
    path('historique/', include('historique.urls')),
    path("equipements/", include("equipements.urls")),

    #calendar
    path("oauth2/login/", start_google_auth, name="google_auth_start"),
    path("oauth2callback", google_auth_callback, name="google_auth_callback"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
