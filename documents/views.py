from django.shortcuts import render
from .models import Contract, TermsOfService
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
# Create your views here.

class TermsOfServiceCreateView(CreateView):
    model = TermsOfService
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Novo Termo de Atendimento',
        'button': 'Criar Termo de Atendimento'
        }
    
class TermsOfServiceUpdateView(UpdateView):
    model = TermsOfService
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Editar Termo de Atendimento',
        'button': 'Atualizar Termo de Atendimento'
        }
    
class TermsOfServiceDetailView(DetailView):
    model = TermsOfService
    template_name = 'documents/detail.html'

class TermsOfServiceListView(ListView):
    model = TermsOfService
    template_name = 'documents/list.html'

class TermsOfServiceDeleteView(DeleteView):
    model = TermsOfService
    template_name = 'documents/confirm_delete.html'
    success_url = reverse_lazy('index')

class ContractCreateView(CreateView):
    model = Contract
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Novo Contrato',
        'button': 'Criar Contrato'
        }
    
class ContractUpdateView(UpdateView):
    model = Contract
    fields = '__all__'
    template_name = 'documents/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Editar Contrato',
        'button': 'Atualizar Contrato'
        }
    
class ContractDetailView(DetailView):
    model = Contract
    template_name = 'documents/detail.html'

class ContractListView(ListView):
    model = Contract
    template_name = 'documents/list.html'

class ContractDeleteView(DeleteView):
    model = Contract
    template_name = 'documents/confirm_delete.html'
    success_url = reverse_lazy('index')