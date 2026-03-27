from django.urls import path

from .views import ContractCreateView, ContractDetailView, ContractListView, ContractUpdateView, TermsOfServiceCreateView, TermsOfServiceDetailView, TermsOfServiceListView, TermsOfServiceUpdateView

urlpatterns = [
    path("cadastrar/termo-de-consentimento/", TermsOfServiceCreateView.as_view(), name="cadastrar_termo_de_consentimento"),
    path("editar/termo-de-consentimento/<int:pk>/", TermsOfServiceUpdateView.as_view(), name="editar_termo_de_consentimento"),
    path("detalhar/termo-de-consentimento/<int:pk>/", TermsOfServiceDetailView.as_view(), name="detalhar_termo_de_consentimento"),
    path("listar/termos-de-consentimento/", TermsOfServiceListView.as_view(), name="listar_termos_de_consentimento"),
    path("cadastrar/contrato/", ContractCreateView.as_view(), name="cadastrar_contrato"),
    path("editar/contrato/<int:pk>/", ContractUpdateView.as_view(), name="editar_contrato"),
    path("detalhar/contrato/<int:pk>/", ContractDetailView.as_view(), name="detalhar_contrato"),
    path("listar/contratos/", ContractListView.as_view(), name="listar_contratos"),
]
