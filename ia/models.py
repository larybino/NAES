from django.conf import settings
from django.db import models
from django.utils import timezone


class AIConfiguration(models.Model):
    name = models.CharField('Nome', max_length=100, default='Configuracao principal')
    provider_url = models.URLField('URL do provedor', default='https://api.openai.com/v1/chat/completions')
    model = models.CharField('Modelo', max_length=100, default='gpt-4o-mini')
    api_key = models.CharField('Chave da API', max_length=500, blank=True)
    system_instructions = models.TextField('Instrucoes do sistema', blank=True)
    monthly_token_limit = models.PositiveIntegerField('Limite mensal de tokens', default=100000)
    is_active = models.BooleanField('Ativa', default=True)
    updated_at = models.DateTimeField('Atualizada em', auto_now=True)

    class Meta:
        verbose_name = 'Configuracao de IA'
        verbose_name_plural = 'Configuracoes de IA'

    def __str__(self):
        return f'{self.name} ({self.model})'


class MonthlyQuota(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ia_quotas')
    month = models.DateField('Mes')
    token_limit = models.PositiveIntegerField('Limite de tokens')
    tokens_used = models.PositiveIntegerField('Tokens usados', default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'month'], name='unique_ia_quota_user_month')]
        ordering = ['-month', 'user__username']

    @property
    def remaining_tokens(self):
        return max(self.token_limit - self.tokens_used, 0)

    @classmethod
    def current_for(cls, user, token_limit):
        month = timezone.localdate().replace(day=1)
        quota, _ = cls.objects.get_or_create(
            user=user,
            month=month,
            defaults={'token_limit': token_limit},
        )
        return quota


class AIRequestAudit(models.Model):
    STATUS_CHOICES = [('success', 'Sucesso'), ('error', 'Erro')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='ia_audits')
    configuration = models.ForeignKey(AIConfiguration, on_delete=models.SET_NULL, null=True, blank=True)
    request_text = models.TextField('Solicitacao')
    response_text = models.TextField('Resposta', blank=True)
    tokens_used = models.PositiveIntegerField('Tokens usados', default=0)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField('Erro', blank=True)
    created_at = models.DateTimeField('Criada em', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Auditoria de chamada IA'
        verbose_name_plural = 'Auditorias de chamadas IA'


class AIConversationMessage(models.Model):
    ROLE_CHOICES = [('user', 'Usuario'), ('assistant', 'Assistente')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ia_messages')
    role = models.CharField('Papel', max_length=20, choices=ROLE_CHOICES)
    content = models.TextField('Conteudo')
    created_at = models.DateTimeField('Criada em', auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Mensagem do assistente'
        verbose_name_plural = 'Mensagens do assistente'
