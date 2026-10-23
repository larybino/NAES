import django_filters
from django.forms import DateInput

from .models import Anamnese, Patient


class PatientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="Nome contém")
    cpf = django_filters.CharFilter(label="CPF contém")
    city = django_filters.CharFilter(label="Cidade contém")
    birth_date = django_filters.DateFilter(
        label="Data de nascimento",
        widget=DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Patient
        fields = {
            "name": ["icontains"],
            "cpf": ["icontains"],
            "city": ["icontains"],
            "birth_date": ["exact"],
        }


def patient_queryset(request):
    if request is None or not request.user.is_authenticated:
        return Patient.objects.none()
    return Patient.objects.filter(user=request.user)


class AnamneseFilter(django_filters.FilterSet):
    patient = django_filters.ModelChoiceFilter(
        queryset=patient_queryset,
        label="Paciente",
    )
    last_dental_visit = django_filters.DateFromToRangeFilter(
        label="Última consulta entre",
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"}),
    )
    uses_floss = django_filters.BooleanFilter(label="Usa fio dental")
    uses_medication = django_filters.BooleanFilter(label="Usa medicamentos")
    drug_allergy = django_filters.BooleanFilter(label="Alergia a medicamentos")
    smokes_or_drugs = django_filters.BooleanFilter(label="Fuma ou usa drogas")

    class Meta:
        model = Anamnese
        fields = {
            "patient": ["exact"],
            "last_dental_visit": ["exact"],
            "uses_floss": ["exact"],
            "uses_medication": ["exact"],
            "drug_allergy": ["exact"],
            "smokes_or_drugs": ["exact"],
        }