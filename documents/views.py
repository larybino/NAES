from django.shortcuts import render
from .models import Contract, TermsOfService
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from website.mixins import BaseLoginMixin, UserOwnedObjectMixin, GroupRequiredMixin

from .filters import ContractFilter, TermsOfServiceFilter

# Create your views here.

class TermsOfServiceCreateView(BaseLoginMixin, UserOwnedObjectMixin, CreateView):
    model = TermsOfService
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('listar_termos_de_consentimento')
    extra_context = {
        'title': 'Novo Termo de Consentimento',
        'button': 'Criar Termo de Consentimento'
        }
    
class TermsOfServiceUpdateView(BaseLoginMixin, UserOwnedObjectMixin, UpdateView):
    model = TermsOfService
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('listar_termos_de_consentimento')
    extra_context = {
        'title': 'Editar Termo de Consentimento',
        'button': 'Atualizar Termo de Consentimento'
        }
    
class TermsOfServiceDetailView(BaseLoginMixin, UserOwnedObjectMixin, DetailView):
    model = TermsOfService
    template_name = 'documents/detail/termofservice.html'
    extra_context = {
        'title': 'Detalhes do Termo de Consentimento'}

class TermsOfServiceListView(BaseLoginMixin, UserOwnedObjectMixin, FilterView):
    model = TermsOfService
    template_name = 'documents/list/termofservice.html'
    extra_context = {
        'title': 'Lista de Termos de Consentimento'}
    paginate_by = 10
    ordering = ['-signature_date', 'patient__name']
    filterset_class = TermsOfServiceFilter

    def get_queryset(self):
        return super().get_queryset().select_related('patient')

class TermsOfServiceDeleteView(BaseLoginMixin, UserOwnedObjectMixin, DeleteView):
    model = TermsOfService
    template_name = 'documents/confirm_delete.html'
    success_url = reverse_lazy('listar_termos_de_consentimento')

class ContractCreateView(GroupRequiredMixin, BaseLoginMixin, UserOwnedObjectMixin, CreateView):
    model = Contract
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('listar_contratos')
    extra_context = {
        'title': 'Novo Contrato',
        'button': 'Criar Contrato'
        }
    group_required = ('staff',)
    
class ContractUpdateView(BaseLoginMixin, UserOwnedObjectMixin, UpdateView):
    model = Contract
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('listar_contratos')
    extra_context = {
        'title': 'Editar Contrato',
        'button': 'Atualizar Contrato'
        }
    
class ContractDetailView(BaseLoginMixin, UserOwnedObjectMixin, DetailView):
    model = Contract
    template_name = 'documents/detail/contract.html'
    extra_context = {
        'title': 'Detalhes do Contrato'}

class ContractListView(BaseLoginMixin, UserOwnedObjectMixin, FilterView):
    model = Contract
    template_name = 'documents/list/contract.html'
    extra_context = {
        'title': 'Lista de Contratos'
    }

    paginate_by = 10
    ordering = ['-signature_date', 'patient__name']
    filterset_class = ContractFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('patient')

class ContractDeleteView(BaseLoginMixin, UserOwnedObjectMixin, DeleteView):
    model = Contract
    template_name = 'documents/confirm_delete.html'
    success_url = reverse_lazy('listar_contratos')