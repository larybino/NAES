from django.urls import path

from .views import (
    AIConfigurationView,
    AIHomeView,
    AIRequestListView,
    AIUserUsageView,
    AssistantMessageView,
    AssistantView,
    MyAIConsumptionView,
)

urlpatterns = [
    path('', AIHomeView.as_view(), name='ia_inicio'),
    path('requisicoes/', AIRequestListView.as_view(), name='ia_requisicoes'),
    path('configuracao/', AIConfigurationView.as_view(), name='ia_configuracao'),
    path('por-usuario/', AIUserUsageView.as_view(), name='ia_por_usuario'),
    path('meu-consumo/', MyAIConsumptionView.as_view(), name='ia_meu_consumo'),
    path('assistente/', AssistantView.as_view(), name='ia_assistente'),
    path('assistente/perguntar/', AssistantMessageView.as_view(), name='ia_perguntar'),
]
