from django.shortcuts import render
from .models import Patient, Anamnese
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView
from website.mixins import BaseLoginMixin, UserOwnedObjectMixin

class PatientCreateView(BaseLoginMixin, UserOwnedObjectMixin, CreateView):
    model = Patient
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('listar_pacientes')
    extra_context = {
        'title': 'Novo Paciente',
        'button': 'Criar Paciente'
        }

class PatientUpdateView(BaseLoginMixin, UserOwnedObjectMixin, UpdateView):
    model = Patient
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('listar_pacientes')
    extra_context = {
        'title': 'Editar Paciente',
        'button': 'Atualizar Paciente'
        }

class PatientDetailView(BaseLoginMixin, UserOwnedObjectMixin, DetailView):
    model = Patient
    template_name = 'pacients/detail/patients.html'
    extra_context = {
        'title': 'Detalhes do Paciente'}

class PatientListView(BaseLoginMixin, UserOwnedObjectMixin, ListView):
    model = Patient
    template_name = 'pacients/list/patients.html'
    extra_context = {
        'title': 'Lista de Pacientes'}

class PatientDeleteView(BaseLoginMixin, UserOwnedObjectMixin, DeleteView):
    model = Patient
    template_name = 'pacients/confirm_delete.html'
    success_url = reverse_lazy('listar_pacientes')

class AnamneseCreateView(BaseLoginMixin, UserOwnedObjectMixin, CreateView):
    model = Anamnese
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('listar_anamneses')
    extra_context = {
        'title': 'Nova Anamnese',
        'button': 'Criar Anamnese'
        }

class AnamneseUpdateView(BaseLoginMixin, UserOwnedObjectMixin, UpdateView):
    model = Anamnese
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('listar_anamneses')
    extra_context = {
        'title': 'Editar Anamnese',
        'button': 'Atualizar Anamnese'
        }

class AnamneseDetailView(BaseLoginMixin, UserOwnedObjectMixin, DetailView):
    model = Anamnese
    template_name = 'pacients/detail/anamnese.html'
    extra_context = {
        'title': 'Detalhes da Anamnese'}


class AnamneseListView(BaseLoginMixin, UserOwnedObjectMixin, ListView):
    model = Anamnese
    template_name = 'pacients/list/anamnese.html'
    extra_context = {
        'title': 'Lista de Anamneses'}

class AnamneseDeleteView(BaseLoginMixin, UserOwnedObjectMixin, DeleteView):
    model = Anamnese
    template_name = 'pacients/confirm_delete.html'
    success_url = reverse_lazy('listar_anamneses')