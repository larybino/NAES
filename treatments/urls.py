from django.urls import path

from .views import PlanItemCreateView, PlanItemDetailView, PlanItemListView, PlanItemUpdateView, TreatmentPerformedCreateView, TreatmentPerformedDetailView, TreatmentPerformedListView, TreatmentPerformedUpdateView, TreatmentPlanCreateView, TreatmentPlanDetailView, TreatmentPlanListView, TreatmentPlanUpdateView

urlpatterns = [
    path("cadastrar/plano-de-tratamento/", TreatmentPlanCreateView.as_view(), name="cadastrar_plano_de_tratamento"),
    path("editar/plano-de-tratamento/<int:pk>/", TreatmentPlanUpdateView.as_view(), name="editar_plano_de_tratamento"),
    path("detalhes/plano-de-tratamento/<int:pk>/", TreatmentPlanDetailView.as_view(), name="detalhes_plano_de_tratamento"),
    path("listar/planos-de-tratamento/", TreatmentPlanListView.as_view(), name="listar_planos_de_tratamento"),
    path("cadastrar/tratamento-realizado/", TreatmentPerformedCreateView.as_view(), name="cadastrar_tratamento_realizado"),
    path("editar/tratamento-realizado/<int:pk>/", TreatmentPerformedUpdateView.as_view(), name="editar_tratamento_realizado"),
    path("detalhes/tratamento-realizado/<int:pk>/", TreatmentPerformedDetailView.as_view(), name="detalhes_tratamento_realizado"),
    path("listar/tratamentos-realizados/", TreatmentPerformedListView.as_view(), name="listar_tratamentos_realizados"),
    path("cadastrar/item-de-plano/", PlanItemCreateView.as_view(), name="cadastrar_item_de_plano"),
    path("editar/item-de-plano/<int:pk>/", PlanItemUpdateView.as_view(), name="editar_item_de_plano"),
    path("detalhes/item-de-plano/<int:pk>/", PlanItemDetailView.as_view(), name="detalhes_item_de_plano"),
    path("listar/itens-de-plano/", PlanItemListView.as_view(), name="listar_itens_de_plano"),
]
