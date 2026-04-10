from django.urls import path, include
from .views import *

urlpatterns = [
    path("cadastrar/paciente/", PatientCreateView.as_view(), name="cadastrar_paciente"),
    path("editar/paciente/<int:pk>/", PatientUpdateView.as_view(), name="editar_paciente"),
    path("detalhes/paciente/<int:pk>/", PatientDetailView.as_view(), name="detalhes_paciente"),
    path("listar/pacientes/", PatientListView.as_view(), name="listar_pacientes"),
    path("deletar/paciente/<int:pk>/", PatientDeleteView.as_view(), name="deletar_paciente"),
    path("cadastrar/anamnese/", AnamneseCreateView.as_view(), name="cadastrar_anamnese"),
    path("editar/anamnese/<int:pk>/", AnamneseUpdateView.as_view(), name="editar_anamnese"),
    path("detalhes/anamnese/<int:pk>/", AnamneseDetailView.as_view(), name="detalhes_anamnese"),
    path("listar/anamneses/", AnamneseListView.as_view(), name="listar_anamneses"),
    path("deletar/anamnese/<int:pk>/", AnamneseDeleteView.as_view(), name="deletar_anamnese"),

]