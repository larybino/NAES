from django.shortcuts import render
from .models import Contract, TermsOfService
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from website.mixins import BaseLoginMixin, UserOwnedObjectMixin

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

class TermsOfServiceListView(BaseLoginMixin, UserOwnedObjectMixin, ListView):
    model = TermsOfService
    template_name = 'documents/list/termofservice.html'
    extra_context = {
        'title': 'Lista de Termos de Consentimento'}

class TermsOfServiceDeleteView(BaseLoginMixin, UserOwnedObjectMixin, DeleteView):
    model = TermsOfService
    template_name = 'documents/confirm_delete.html'
    success_url = reverse_lazy('listar_termos_de_consentimento')

class ContractCreateView(BaseLoginMixin, UserOwnedObjectMixin, CreateView):
    model = Contract
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('listar_contratos')
    extra_context = {
        'title': 'Novo Contrato',
        'button': 'Criar Contrato'
        }
    
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

class ContractListView(BaseLoginMixin, UserOwnedObjectMixin, ListView):
    model = Contract
    template_name = 'documents/list/contract.html'
    extra_context = {
        'title': 'Lista de Contratos'
    }

class ContractDeleteView(BaseLoginMixin, UserOwnedObjectMixin, DeleteView):
    model = Contract
    template_name = 'documents/confirm_delete.html'
    success_url = reverse_lazy('listar_contratos')