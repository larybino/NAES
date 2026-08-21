from django.shortcuts import render
from .models import TreatmentPerformed, TreatmentPlan, PlanItem
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from website.mixins import BaseLoginMixin, UserOwnedObjectMixin

class TreatmentPlanCreateView(BaseLoginMixin, UserOwnedObjectMixin, CreateView):
    model = TreatmentPlan
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_planos_de_tratamento')
    extra_context = {
        'title': 'Novo Plano de Tratamento',
        'button': 'Criar Plano de Tratamento'
        }
    
class TreatmentPlanUpdateView(BaseLoginMixin, UserOwnedObjectMixin, UpdateView):
    model = TreatmentPlan
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_planos_de_tratamento')
    extra_context = {
        'title': 'Editar Plano de Tratamento',
        'button': 'Atualizar Plano de Tratamento'
        }
    
class TreatmentPlanDetailView(BaseLoginMixin, UserOwnedObjectMixin, DetailView):
    model = TreatmentPlan
    template_name = 'treatments/detail/treatmentplan.html'   
    extra_context = {
        'title': 'Detalhes do Plano de Tratamento'}

class TreatmentPlanListView(BaseLoginMixin, UserOwnedObjectMixin, ListView):
    model = TreatmentPlan
    template_name = 'treatments/list/treatmentplan.html'
    paginate_by = 10
    extra_context = {
        'title': 'Lista de Planos de Tratamento'}
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('patient')

class TreatmentPlanDeleteView(BaseLoginMixin, UserOwnedObjectMixin, DeleteView):
    model = TreatmentPlan
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_planos_de_tratamento')

class TreatmentPerformedCreateView(BaseLoginMixin, UserOwnedObjectMixin, CreateView):
    model = TreatmentPerformed
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_tratamentos_realizados')
    extra_context = {
        'title': 'Novo Tratamento Realizado',
        'button': 'Criar Tratamento Realizado'
        }

class TreatmentPerformedUpdateView(BaseLoginMixin, UserOwnedObjectMixin, UpdateView):
    model = TreatmentPerformed
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_tratamentos_realizados')
    extra_context = {
        'title': 'Editar Tratamento Realizado',
        'button': 'Atualizar Tratamento Realizado'
        }   

class TreatmentPerformedDetailView(BaseLoginMixin, UserOwnedObjectMixin, DetailView):
    model = TreatmentPerformed
    template_name = 'treatments/detail/treatmentperfomed.html'
    extra_context = {
        'title': 'Detalhes do Tratamento Realizado'}

class TreatmentPerformedListView(BaseLoginMixin, UserOwnedObjectMixin, ListView):
    model = TreatmentPerformed
    template_name = 'treatments/list/treatmentperfomed.html'
    paginate_by = 10
    extra_context = {
        'title': 'Lista de Tratamentos Realizados'}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('treatment_plan__patient')

class TreatmentPerformedDeleteView(BaseLoginMixin, UserOwnedObjectMixin, DeleteView):
    model = TreatmentPerformed
    template_name = 'treatments/confirm_delete.html'
    success_url = reverse_lazy('listar_tratamentos_realizados')

class PlanItemCreateView(BaseLoginMixin, UserOwnedObjectMixin, CreateView):
    model = PlanItem
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_itens_do_plano')
    extra_context = {
        'title': 'Novo Item do Plano',
        'button': 'Criar Item do Plano'
        }
    
class PlanItemUpdateView(BaseLoginMixin, UserOwnedObjectMixin, UpdateView):
    model = PlanItem
    fields = '__all__'
    template_name = 'treatments/form.html'
    success_url = reverse_lazy('listar_itens_do_plano')
    extra_context = {
        'title': 'Editar Item do Plano',
        'button': 'Atualizar Item do Plano'
        }
    
class PlanItemDetailView(BaseLoginMixin, UserOwnedObjectMixin, DetailView):
    model = PlanItem
    template_name = 'treatments/detail/planitem.html'
    extra_context = {
        'title': 'Detalhes do Item do Plano'}

class PlanItemListView(BaseLoginMixin, UserOwnedObjectMixin, ListView):
    model = PlanItem
    template_name = 'treatments/list/planitem.html'
    paginate_by = 10
    extra_context = {
        'title': 'Lista de Itens do Plano'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('treatment_plan__patient')

class PlanItemDeleteView(BaseLoginMixin, UserOwnedObjectMixin, DeleteView):
    model = PlanItem
    template_name = 'treatments/confirm_delete.html'
    success_url = reverse_lazy('listar_itens_do_plano')
