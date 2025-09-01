from django.urls import path
from dashboard import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "dashboard"

urlpatterns = [
    path("usuarios/", views.visitante, name="usuarios"),
    path("administradores/", views.administrador, name="administradores"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
