from django.shortcuts import render
from .models import TreatmentPerformed, TreatmentPlan, PlanItem
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

class TreatmentPlanCreateView(CreateView):
    model = TreatmentPlan
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_planos_de_tratamento')
    extra_context = {
        'title': 'Novo Plano de Tratamento',
        'button': 'Criar Plano de Tratamento'
        }
    
class TreatmentPlanUpdateView(UpdateView):
    model = TreatmentPlan
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_planos_de_tratamento')
    extra_context = {
        'title': 'Editar Plano de Tratamento',
        'button': 'Atualizar Plano de Tratamento'
        }
    
class TreatmentPlanDetailView(DetailView):
    model = TreatmentPlan
    template_name = 'treatments/detail.html'   
    extra_context = {
        'title': 'Detalhes do Plano de Tratamento'}

class TreatmentPlanListView(ListView):
    model = TreatmentPlan
    template_name = 'treatments/list.html'
    extra_context = {
        'title': 'Lista de Planos de Tratamento'}

class TreatmentPlanDeleteView(DeleteView):
    model = TreatmentPlan
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_planos_de_tratamento')

class TreatmentPerformedCreateView(CreateView):
    model = TreatmentPerformed
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_tratamentos_realizados')
    extra_context = {
        'title': 'Novo Tratamento Realizado',
        'button': 'Criar Tratamento Realizado'
        }

class TreatmentPerformedUpdateView(UpdateView):
    model = TreatmentPerformed
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_tratamentos_realizados')
    extra_context = {
        'title': 'Editar Tratamento Realizado',
        'button': 'Atualizar Tratamento Realizado'
        }   

class TreatmentPerformedDetailView(DetailView):
    model = TreatmentPerformed
    template_name = 'treatments/detail.html'
    extra_context = {
        'title': 'Detalhes do Tratamento Realizado'}

class TreatmentPerformedListView(ListView):
    model = TreatmentPerformed
    template_name = 'treatments/list.html'
    extra_context = {
        'title': 'Lista de Tratamentos Realizados'}

class TreatmentPerformedDeleteView(DeleteView):
    model = TreatmentPerformed
    template_name = 'treatments/confirm_delete.html'
    success_url = reverse_lazy('listar_tratamentos_realizados')

class PlanItemCreateView(CreateView):
    model = PlanItem
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_itens_do_plano')
    extra_context = {
        'title': 'Novo Item do Plano',
        'button': 'Criar Item do Plano'
        }
    
class PlanItemUpdateView(UpdateView):
    model = PlanItem
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_itens_do_plano')
    extra_context = {
        'title': 'Editar Item do Plano',
        'button': 'Atualizar Item do Plano'
        }
    
class PlanItemDetailView(DetailView):
    model = PlanItem
    template_name = 'treatments/detail.html'
    extra_context = {
        'title': 'Detalhes do Item do Plano'}

class PlanItemListView(ListView):
    model = PlanItem
    template_name = 'treatments/list.html'
    extra_context = {
        'title': 'Lista de Itens do Plano'
    }

class PlanItemDeleteView(DeleteView):
    model = PlanItem
    template_name = 'treatments/confirm_delete.html'
    success_url = reverse_lazy('listar_itens_do_plano')
