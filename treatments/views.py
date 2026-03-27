from django.shortcuts import render
from .models import TreatmentPerformed, TreatmentPlan, PlanItem
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView

class TreatmentPlanCreateView(CreateView):
    model = TreatmentPlan
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Novo Plano de Tratamento',
        'button': 'Criar Plano de Tratamento'
        }
    
class TreatmentPlanUpdateView(UpdateView):
    model = TreatmentPlan
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Editar Plano de Tratamento',
        'button': 'Atualizar Plano de Tratamento'
        }
    
class TreatmentPlanDetailView(DetailView):
    model = TreatmentPlan
    template_name = 'treatments/detail.html'   

class TreatmentPlanListView(ListView):
    model = TreatmentPlan
    template_name = 'treatments/list.html'

class TreatmentPerformedCreateView(CreateView):
    model = TreatmentPerformed
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Novo Tratamento Realizado',
        'button': 'Criar Tratamento Realizado'
        }

class TreatmentPerformedUpdateView(UpdateView):
    model = TreatmentPerformed
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Editar Tratamento Realizado',
        'button': 'Atualizar Tratamento Realizado'
        }   

class TreatmentPerformedDetailView(DetailView):
    model = TreatmentPerformed
    template_name = 'treatments/detail.html'

class TreatmentPerformedListView(ListView):
    model = TreatmentPerformed
    template_name = 'treatments/list.html'

class PlanItemCreateView(CreateView):
    model = PlanItem
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Novo Item do Plano',
        'button': 'Criar Item do Plano'
        }
    
class PlanItemUpdateView(UpdateView):
    model = PlanItem
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Editar Item do Plano',
        'button': 'Atualizar Item do Plano'
        }
    
class PlanItemDetailView(DetailView):
    model = PlanItem
    template_name = 'treatments/detail.html'

class PlanItemListView(ListView):
    model = PlanItem
    template_name = 'treatments/list.html'
