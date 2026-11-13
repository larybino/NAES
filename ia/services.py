import json
import urllib.error
import urllib.request

from django.db import transaction
from django.utils import timezone

from .models import AIConfiguration, AIConversationMessage, AIRequestAudit, MonthlyQuota


class AIServiceError(Exception):
    pass


def _active_configuration():
    configuration = AIConfiguration.objects.filter(is_active=True).order_by('-updated_at').first()
    if not configuration or not configuration.api_key:
        raise AIServiceError('Configure um provedor e uma chave de API antes de usar o assistente.')
    return configuration


def _extract_response(payload):
    try:
        return payload['choices'][0]['message']['content'], int(payload.get('usage', {}).get('total_tokens', 0))
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise AIServiceError('Resposta invalida do provedor de IA.') from exc


def chamar_ia(user, messages, context=''):
    """Single gateway for all provider calls, quota accounting and audit logging."""
    configuration = _active_configuration()
    with transaction.atomic():
        quota = MonthlyQuota.objects.select_for_update().filter(
            user=user, month=timezone.localdate().replace(day=1)
        ).first()
        if quota is None:
            quota = MonthlyQuota.objects.create(
                user=user,
                month=timezone.localdate().replace(day=1),
                token_limit=configuration.monthly_token_limit,
            )
        if quota.tokens_used >= quota.token_limit:
            raise AIServiceError('A cota mensal de tokens foi atingida.')

        system_text = configuration.system_instructions.strip()
        if context:
            system_text = f'{system_text}\n\nContexto do projeto:\n{context}'.strip()
        payload_messages = ([{'role': 'system', 'content': system_text}] if system_text else []) + messages[-5:]
        body = json.dumps({'model': configuration.model, 'messages': payload_messages}).encode('utf-8')
        request = urllib.request.Request(
            configuration.provider_url,
            data=body,
            headers={'Authorization': f'Bearer {configuration.api_key}', 'Content-Type': 'application/json'},
            method='POST',
        )
        audit = AIRequestAudit.objects.create(
            user=user,
            configuration=configuration,
            request_text=messages[-1].get('content', '') if messages else '',
            status='error',
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                answer, tokens = _extract_response(json.loads(response.read().decode('utf-8')))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, AIServiceError) as exc:
            audit.error_message = str(exc)
            audit.save(update_fields=['error_message'])
            raise AIServiceError(f'Nao foi possivel chamar a IA: {exc}') from exc

        quota.tokens_used = min(quota.token_limit, quota.tokens_used + tokens)
        quota.save(update_fields=['tokens_used'])
        audit.response_text = answer
        audit.tokens_used = tokens
        audit.status = 'success'
        audit.save(update_fields=['response_text', 'tokens_used', 'status'])
        return answer, tokens


def testar_conexao(user):
    return chamar_ia(user, [{'role': 'user', 'content': 'Responda somente: conexao OK'}])


def save_conversation_message(user, role, content):
    return AIConversationMessage.objects.create(user=user, role=role, content=content)
