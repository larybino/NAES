from pathlib import Path

import bleach
import markdown
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import FormView, ListView, TemplateView

from .forms import AIConfigurationForm
from .models import AIConfiguration, AIConversationMessage, AIRequestAudit, MonthlyQuota
from .services import AIServiceError, chamar_ia, save_conversation_message, testar_conexao


class StaffAIRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff


class AIHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'ia/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['configuration'] = AIConfiguration.objects.filter(is_active=True).first()
        limit = context['configuration'].monthly_token_limit if context['configuration'] else 0
        context['quota'] = MonthlyQuota.current_for(self.request.user, limit)
        context['recent_audits'] = AIRequestAudit.objects.filter(user=self.request.user)[:5]
        return context


class AIRequestListView(LoginRequiredMixin, ListView):
    model = AIRequestAudit
    template_name = 'ia/requests.html'
    context_object_name = 'requests'
    paginate_by = 20

    def get_queryset(self):
        queryset = AIRequestAudit.objects.select_related('user', 'configuration')
        return queryset if self.request.user.is_staff else queryset.filter(user=self.request.user)


class AIConfigurationView(StaffAIRequiredMixin, FormView):
    template_name = 'ia/configuration.html'
    form_class = AIConfigurationForm
    success_url = '/ia/configuracao/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = AIConfiguration.objects.filter(is_active=True).first()
        return kwargs

    def form_valid(self, form):
        configuration = form.save(commit=False)
        configuration.is_active = True
        configuration.save()
        messages.success(self.request, 'Configuracao de IA salva com sucesso.')
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'test':
            try:
                answer, tokens = testar_conexao(request.user)
                messages.success(request, f'Conexao funcionando: {answer} ({tokens} tokens).')
            except AIServiceError as exc:
                messages.error(request, str(exc))
            return redirect('ia_configuracao')
        return super().post(request, *args, **kwargs)


class AIUserUsageView(LoginRequiredMixin, ListView):
    model = MonthlyQuota
    template_name = 'ia/user_usage.html'
    context_object_name = 'quotas'

    def get_queryset(self):
        queryset = MonthlyQuota.objects.select_related('user')
        return queryset if self.request.user.is_staff else queryset.filter(user=self.request.user)


class MyAIConsumptionView(LoginRequiredMixin, TemplateView):
    template_name = 'ia/my_consumption.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        configuration = AIConfiguration.objects.filter(is_active=True).first()
        limit = configuration.monthly_token_limit if configuration else 0
        context['quota'] = MonthlyQuota.current_for(self.request.user, limit)
        context['audits'] = AIRequestAudit.objects.filter(user=self.request.user)[:20]
        return context


class AssistantView(LoginRequiredMixin, TemplateView):
    template_name = 'ia/assistant.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = list(
            AIConversationMessage.objects.filter(user=self.request.user).order_by('-created_at')[:20]
        )[::-1]
        return context


class AssistantMessageView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        question = request.POST.get('question', '').strip()
        if not question or len(question) > 4000:
            return JsonResponse({'error': 'Informe uma pergunta com ate 4000 caracteres.'}, status=400)
        save_conversation_message(request.user, 'user', question)
        messages_for_ai = list(
            AIConversationMessage.objects.filter(user=request.user)
            .order_by('-created_at')[:5]
        )
        messages_for_ai.reverse()
        payload = [{'role': item.role, 'content': item.content} for item in messages_for_ai]
        context_path = Path(settings.BASE_DIR) / 'contexto_projeto.md'
        context = context_path.read_text(encoding='utf-8') if context_path.exists() else ''
        try:
            answer, tokens = chamar_ia(request.user, payload, context)
        except AIServiceError as exc:
            return JsonResponse({'error': str(exc)}, status=503)
        save_conversation_message(request.user, 'assistant', answer)
        rendered = markdown.markdown(answer, extensions=['extra', 'sane_lists'])
        rendered = bleach.clean(
            rendered,
            tags=['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'h1', 'h2', 'h3', 'a'],
            attributes={'a': ['href', 'title', 'rel']},
            protocols=['http', 'https'],
        )
        return JsonResponse({'answer_html': rendered, 'tokens': tokens})
