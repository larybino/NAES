from django.shortcuts import render
from .models import Patient, Anamnese
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView


class PatientCreateView(CreateView):
    model = Patient
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('listar_pacientes')
    extra_context = {
        'title': 'Novo Paciente',
        'button': 'Criar Paciente'
        }

class PatientUpdateView(UpdateView):
    model = Patient
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('listar_pacientes')
    extra_context = {
        'title': 'Editar Paciente',
        'button': 'Atualizar Paciente'
        }

class PatientDetailView(DetailView):
    model = Patient
    template_name = 'pacients/detail/patients.html'
    extra_context = {
        'title': 'Detalhes do Paciente'}

class PatientListView(ListView):
    model = Patient
    template_name = 'pacients/list/patients.html'
    extra_context = {
        'title': 'Lista de Pacientes'}

class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'pacients/confirm_delete.html'
    success_url = reverse_lazy('listar_pacientes')

class AnamneseCreateView(CreateView):
    model = Anamnese
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('listar_anamneses')
    extra_context = {
        'title': 'Nova Anamnese',
        'button': 'Criar Anamnese'
        }

class AnamneseUpdateView(UpdateView):
    model = Anamnese
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('listar_anamneses')
    extra_context = {
        'title': 'Editar Anamnese',
        'button': 'Atualizar Anamnese'
        }

class AnamneseDetailView(DetailView):
    model = Anamnese
    template_name = 'pacients/detail/anamnese.html'
    extra_context = {
        'title': 'Detalhes da Anamnese'}


class AnamneseListView(ListView):
    model = Anamnese
    template_name = 'pacients/list/anamnese.html'
    extra_context = {
        'title': 'Lista de Anamneses'}

class AnamneseDeleteView(DeleteView):
    model = Anamnese
    template_name = 'pacients/confirm_delete.html'
    success_url = reverse_lazy('listar_anamneses')