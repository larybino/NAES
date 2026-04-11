from django.shortcuts import render
from .models import Contract, TermsOfService
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
# Create your views here.

class TermsOfServiceCreateView(CreateView):
    model = TermsOfService
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('listar_termos_de_atendimento')
    extra_context = {
        'title': 'Novo Termo de Atendimento',
        'button': 'Criar Termo de Atendimento'
        }
    
class TermsOfServiceUpdateView(UpdateView):
    model = TermsOfService
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('listar_termos_de_atendimento')
    extra_context = {
        'title': 'Editar Termo de Atendimento',
        'button': 'Atualizar Termo de Atendimento'
        }
    
class TermsOfServiceDetailView(DetailView):
    model = TermsOfService
    template_name = 'documents/detail.html'
    extra_context = {
        'title': 'Detalhes do Termo de Atendimento'}

class TermsOfServiceListView(ListView):
    model = TermsOfService
    template_name = 'documents/list.html'
    extra_context = {
        'title': 'Lista de Termos de Atendimento'}

class TermsOfServiceDeleteView(DeleteView):
    model = TermsOfService
    template_name = 'documents/confirm_delete.html'
    success_url = reverse_lazy('listar_termos_de_atendimento')

class ContractCreateView(CreateView):
    model = Contract
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('listar_contratos')
    extra_context = {
        'title': 'Novo Contrato',
        'button': 'Criar Contrato'
        }
    
class ContractUpdateView(UpdateView):
    model = Contract
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('listar_contratos')
    extra_context = {
        'title': 'Editar Contrato',
        'button': 'Atualizar Contrato'
        }
    
class ContractDetailView(DetailView):
    model = Contract
    template_name = 'documents/detail.html'
    extra_context = {
        'title': 'Detalhes do Contrato'}

class ContractListView(ListView):
    model = Contract
    template_name = 'documents/list.html'
    extra_context = {
        'title': 'Lista de Contratos'
    }

class ContractDeleteView(DeleteView):
    model = Contract
    template_name = 'documents/confirm_delete.html'
    success_url = reverse_lazy('listar_contratos')