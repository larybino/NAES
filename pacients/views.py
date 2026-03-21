from django.shortcuts import render
from .models import Patient, Anamnese
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView


class PatientCreateView(CreateView):
    model = Patient
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Novo Paciente',
        'button': 'Criar Paciente'
        }

class PatientUpdateView(UpdateView):
    model = Patient
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Editar Paciente',
        'button': 'Atualizar Paciente'
        }

class PatientDetailView(DetailView):
    model = Patient
    template_name = 'pacients/detail.html'

class PatientListView(ListView):
    model = Patient
    template_name = 'pacients/list.html'

class AnamneseCreateView(CreateView):
    model = Anamnese
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Nova Anamnese',
        'button': 'Criar Anamnese'
        }

class AnamneseUpdateView(UpdateView):
    model = Anamnese
    fields = '__all__'
    template_name = 'pacients/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Editar Anamnese',
        'button': 'Atualizar Anamnese'
        }

class AnamneseDetailView(DetailView):
    model = Anamnese
    template_name = 'pacients/detail.html'


class AnamneseListView(ListView):
    model = Anamnese
    template_name = 'pacients/list.html'

